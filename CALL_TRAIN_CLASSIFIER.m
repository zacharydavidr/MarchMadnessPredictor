function TRN_CLS_MDL = CALL_TRAIN_CLASSIFIER(DAT_SET_TBL,SEL_FET_IND,NUM_TRN_CLS,NUM_VAL_FLD,NUM_PCA_CMP)
% -------------------------------------------------------------------------
% 
% -------------------------------------------------------------------------
% INPUT: DAT_SET_TBL IS A TABEL OF TRAINING FEATURES AND CLASS-LABELES
% OUTPUT: TRN_KNN_MDL IS STRUCT OF TRAINED CLASSIFER
% MDL_VAL_ACU: THE REPORTED VALIDATION ACCURACY
%
% TESTING: USE TRN_KNN_MDL.MDL_CLS_FUN(TST_SET_TBL) WITH AN INPUT OF TESTING TABEL
% TST_SET_TBL MUST BE AT THE SAME SIZE AS DAT_SET_TBL OR WITH MORE FEATURES
% -------------------------------------------------------------------------
% EXTRACT: FEATURES AND THEIR CORRESPONDING CLASS-LABELS FOR TRAINING
% -------------------------------------------------------------------------
  DAT_FET_NAM = {'AdjTempo','RankAdjTempo','AdjOE','RankAdjOE','AdjDE','RankAdjDE','AdjEM','RankAdjEM','seed','offensivereboundingpct','totalreboundingpercentage','opponentftmper100possessions','threepointpct','opponentshootingpct','winpctclosegames','opponenteffectivefieldgoalpct','pointsfrom3pointers','pointsfrom2pointers','winpctallgames','freethrowpct','freethrowsmadepergame','assistperturnoverratio','personalfoulsperpossession','trueshootingpercentage','RPIRank'};
  DAT_FET_TBL = DAT_SET_TBL(:,DAT_FET_NAM);
  TRN_SET_CLS = DAT_SET_TBL.Class;
% -------------------------------------------------------------------------
% EXTRACT: SELECTED FEATURES 
% -------------------------------------------------------------------------
  SEL_FET_SWT = false(1,size(DAT_FET_TBL,2));
  SEL_FET_SWT(SEL_FET_IND) = true;
% -------------------------------------------------------------------------
% PERFORM: DATA TRANSFORMATION USING PCA AFTER EXCLUDING ESSINTIAL FEATURES
% -------------------------------------------------------------------------
  [PCA_FET_TBL] = DAT_FET_TBL(:,~SEL_FET_SWT);
  [PCA_FET_TBL] = table2array(varfun(@double,PCA_FET_TBL));
  [PCA_FET_TBL(isinf(PCA_FET_TBL))] = NaN; % INF FEATURE VALUES CONSIDERED AS MISSING
  [PCA_COF_MAT,PCA_SCR_MAT,~,~,~,PCA_CEN_MAT] = pca(PCA_FET_TBL,'NumComponents',NUM_PCA_CMP);
  [TRN_FET_TBL] = [array2table(PCA_SCR_MAT(:,:)), DAT_FET_TBL(:,SEL_FET_SWT)];
% -------------------------------------------------------------------------
% PERFORM: TRAINING
% -------------------------------------------------------------------------
  TRN_KNN_MDL = fitcknn(TRN_FET_TBL,TRN_SET_CLS,'Distance','Euclidean','Exponent',[],'NumNeighbors',10,'DistanceWeight','SquaredInverse','Standardize',true,'ClassNames',categorical({'C'; 'CG'; 'DNQ'; 'E8'; 'FF'; 'R32'; 'R64'; 'S16'}));
% -------------------------------------------------------------------------
% BUILD: CLASSIFIER STRUCT OF FUNCTIONS
% -------------------------------------------------------------------------
  EXT_NAM_FUN = @(X,Y) X(:,Y); % FEATURE EXTRACTION FUNCTION
  PCA_TRN_FUN = @(X) [array2table((table2array(varfun(@double,X(:,~SEL_FET_SWT))) - PCA_CEN_MAT) * PCA_COF_MAT),X(:,SEL_FET_SWT)];
  KNN_CLS_FUN = @(X) predict(TRN_KNN_MDL,X);
  TRN_CLS_MDL.MDL_CLS_FUN = @(X,Y) KNN_CLS_FUN(PCA_TRN_FUN(EXT_NAM_FUN(X,Y)));
% -------------------------------------------------------------------------
% PREPAIR: TRN_KNN_MDL STRUCT FEILDS
% -------------------------------------------------------------------------
  TRN_CLS_MDL.DAT_FET_NAM = DAT_FET_NAM;
  TRN_CLS_MDL.PCA_CEN_MAT = PCA_CEN_MAT;
  TRN_CLS_MDL.PCACoefficients = PCA_COF_MAT;
  TRN_CLS_MDL.TRN_KNN_MDL = TRN_KNN_MDL;
  TRN_CLS_MDL.TRN_MDL_HLP = 'THIS STRUCT IS A TRAINED MODEL TO PREDICT NCAA CHAMPIONSHIP RESULTS FOR 2018';
  TRN_CLS_MDL.HOW_PRF_PRD = sprintf('TO MAKE TESTING ON NEW DATA USE: MDL_RES_MAT = c.MDL_CLS_FUN(TST_SET_TBL) \nreplacing ''c'' with the name of the variable that is this struct, e.g. ''trainedModel''. \n \nThe table, T, must contain the variables returned by: \n  c.DAT_FET_NAM \nVariable formats (e.g. matrix/vector, datatype) must match the original training data. \nAdditional variables are ignored. \n \nFor more information, see <a href="matlab:helpview(fullfile(docroot, ''stats'',''stats.map''),''appclassification_exportmodeltoworkspace'')">How to predict using an exported model</a>.');
% -------------------------------------------------------------------------
% PERFORM: CROSS VALIDATION
% -------------------------------------------------------------------------
  FLD_PRT_TBL = cvpartition(TRN_SET_CLS,'KFold',NUM_VAL_FLD); % CROSS VALIDATION FOLD INDICES
  FLD_CLS_PRD = categorical(nan(size(TRN_SET_CLS)));
  FLD_SCR_MAT = NaN(size(TRN_FET_TBL,1),NUM_TRN_CLS);
  PRC_SGN_CHR = '%';
  fprintf('PER-FOLD TRAINING ACCURACY\n');
  for F = 1:1:NUM_VAL_FLD
      % -------------------------------------------------------------------
      % FIND: FOLD TRAINING FEATURE AND CLASS TABELS
      % -------------------------------------------------------------------
        FLD_FET_TBL = DAT_FET_TBL(FLD_PRT_TBL.training(F),:);
        FLD_CLS_TBL = TRN_SET_CLS(FLD_PRT_TBL.training(F),:);
      % -------------------------------------------------------------------
      % PERFORM: FOLD TRANSFORMATION USING PCA AFTER EXCLUDING ESSINTIAL FEATURES
      % -------------------------------------------------------------------
        [SEL_FET_SWT] = false(1,size(DAT_FET_TBL,2));
        [SEL_FET_SWT(SEL_FET_IND)] = true;
        [PCA_FET_TBL] = FLD_FET_TBL(:,~SEL_FET_SWT);
        [PCA_FET_TBL] = table2array(varfun(@double,PCA_FET_TBL));
        [PCA_FET_TBL(isinf(PCA_FET_TBL))] = NaN;
        [PCA_COF_MAT,PCA_SCR_MAT,~,~,~,PCA_CEN_MAT] = pca(PCA_FET_TBL,'NumComponents',NUM_PCA_CMP);
        [FLD_FET_TBL] = [array2table(PCA_SCR_MAT(:,:)),FLD_FET_TBL(:,SEL_FET_SWT)];
      % -------------------------------------------------------------------
      % PERFORM: TRAINING ON FOLDS
      % -------------------------------------------------------------------
        FLD_CLS_MDL = fitcknn(FLD_FET_TBL,FLD_CLS_TBL,'Distance','Euclidean','Exponent',[],'NumNeighbors',10,'DistanceWeight','SquaredInverse','Standardize',true,'ClassNames',categorical({'C';'CG';'DNQ';'E8';'FF';'R32';'R64';'S16'}));
      % -------------------------------------------------------------------
      % PREPAIR: TRN_KNN_MDL STRUCT FEILDS
      % -------------------------------------------------------------------
        [PCA_TRN_FUN] = @(X) [array2table((table2array(varfun(@double,X(:,~SEL_FET_SWT))) - PCA_CEN_MAT) * PCA_COF_MAT),X(:,SEL_FET_SWT)];
      % -------------------------------------------------------------------
      % FIND: FOLD PREDICTIONS AND FOR EACH TESTING SAMLE ITS PERCLASS SCORE AND TEST
      % -------------------------------------------------------------------
        [FLD_CLS_PRD(FLD_PRT_TBL.test(F),:),FLD_SCR_MAT(FLD_PRT_TBL.test(F),:)] = predict(FLD_CLS_MDL,PCA_TRN_FUN(DAT_FET_TBL(FLD_PRT_TBL.test(F),:)));
      % -------------------------------------------------------------------
      % FIND: PER-FOLD TRAINING ACCURACY
      % -------------------------------------------------------------------
        FLD_TRU_PRD = FLD_CLS_PRD(FLD_PRT_TBL.test(F)) == TRN_SET_CLS(FLD_PRT_TBL.test(F));
        FLD_TRU_PRD = FLD_TRU_PRD(~ismissing(TRN_SET_CLS(FLD_PRT_TBL.test(F))));
        fprintf('FOLD: %03.2f%s\n',(100* sum(FLD_TRU_PRD)) / length(FLD_TRU_PRD),PRC_SGN_CHR);
  end
% -------------------------------------------------------------------------
% FIND: CROSS-VALIDATION ACCURACY
% -------------------------------------------------------------------------
  TRN_TRU_PRD = FLD_CLS_PRD == TRN_SET_CLS;
  TRN_TRU_PRD = TRN_TRU_PRD(~ismissing(TRN_SET_CLS));
  fprintf('\n');
  fprintf('TRAINING ACUURACY: %03.2f%s\n',(100* sum(TRN_TRU_PRD)) / length(TRN_TRU_PRD),PRC_SGN_CHR);
end
