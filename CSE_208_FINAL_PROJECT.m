% -------------------------------------------------------------------------
% CSE802: FINAL PROJECT - FEATURE ANALYSIS
% -------------------------------------------------------------------------
  clear
  close all
  clc
% -------------------------------------------------------------------------
% PERFORM: FEATURE EXTRACTION
% -------------------------------------------------------------------------
  TRN_SET_TBL = readtable('master.csv');
  TRN_SET_MAT = nan(size(TRN_SET_TBL,1),size(TRN_SET_TBL,2) - 7);  
  TRN_SET_MAT(:,[1 3:27]) = [table2array(TRN_SET_TBL(:,1)) table2array(TRN_SET_TBL(:,3:27))];
  
  TRN_SET_CLS = {'DNQ','R64','R32','S16','E8','FF','CG','C'}; % THE CHAMPIONSHIP CLASSES
  for I = 1:1:length(TRN_SET_CLS)
      TRN_SET_MAT(strcmp(TRN_SET_TBL.Class,TRN_SET_CLS{I}),end) = I;
  end
  DAT_SET_TEM = unique(TRN_SET_TBL.Team); % THE CHAMPIONSHIP TEAMS
  for I = 1:1:length(DAT_SET_TEM)
      TRN_SET_MAT(strcmp(TRN_SET_TBL.Team,DAT_SET_TEM{I}),2) = I;
  end
  HST_BIN_WDT = [2 20 2 20 2 20 5 20 1 2 1 1 1 1 0.05 0.05 2 1 0.05 1 0.75 0.5 1 2 15];
  DAT_SET_FET = readtable('DAT_SET_FET.csv','Delimiter',',');
  for F = 3:1:27
      figure
      for C = 1:1:length(TRN_SET_CLS)
          subaxis(2,4,C,'Spacing',0.03,'Padding',0,'Margin',0.07);
          H = histogram(TRN_SET_MAT(TRN_SET_MAT(:,end) == C,F),'Normalization','PDF','BinWidth',HST_BIN_WDT(F - 2),'BinLimits',[min(TRN_SET_MAT(:,F)) - (0.5 * HST_BIN_WDT(F - 2))  max(TRN_SET_MAT(:,F)) + (0.5 * HST_BIN_WDT(F - 2))]); set(H,'FaceColor','K');
          if (C > 4)
              xlabel(DAT_SET_FET.Feature_Name{F - 2},'Interpreter','Latex');
          else
              set(gca,'XTickLabel',[]);
          end
          if (C == 1 || C == 5)
              ylabel('Probabilty','Interpreter','Latex');              
          end
          L = legend(TRN_SET_CLS{C}); set(L,'Box','Off','Color','None','Location','Best','Interpreter','Latex');
          box off
      end
  end
% -------------------------------------------------------------------------
% PERFORM: TRAINING VIA K-FOLD CROSS VALIDATION
% -------------------------------------------------------------------------
  SEL_FET_IND = [6 8 9 15 19 22 23]; %  NON-TRANSFORMED FEATURE INDICES
  NUM_PCA_CMP = 5; % NUMBER OF PCA COMPONENTS. THIS WILL BE EQUAL TO THE TOTAL NUMBER OF FEATURES MINUS NUMBER OF SELECTED ONES
  NUM_VAL_FLD = 10; % NUMBER OF CROSS-VALIDATION FOLDS
  TRN_CLS_MDL = CALL_TRAIN_CLASSIFIER(TRN_SET_TBL,SEL_FET_IND,length(TRN_SET_CLS),NUM_VAL_FLD,NUM_PCA_CMP);
% -------------------------------------------------------------------------
% PERFORM: TESTING ON 2018 FEATURE SET
% -------------------------------------------------------------------------
  TST_SET_TBL = readtable('out_2018.csv');
  MDL_CLS_PRD = TRN_CLS_MDL.MDL_CLS_FUN(TST_SET_TBL,TRN_CLS_MDL.DAT_FET_NAM);
% -------------------------------------------------------------------------
% DISPLAY: PREDICTION RESULTS
% -------------------------------------------------------------------------
  TEM_PER_CLS = cell(1,length(TRN_SET_CLS));
  fprintf('\n');
  fprintf('TEAMS PER-CLASS\n');
  for I = 1:1:length(TRN_SET_CLS)
      TEM_PER_CLS{I} = TST_SET_TBL.TeamName(MDL_CLS_PRD == TRN_SET_CLS{I});
      fprintf('Class %s: ',TRN_SET_CLS{I}); disp(TEM_PER_CLS{I}'); fprintf('\n');
  end