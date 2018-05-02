test_data = readtable("test_2018.csv");

model_yfit = model1.predictFcn(test_data);
modle_accuracy = sum(model_yfit==table2array(test_data(:,end)))/size(model_yfit,1);
model_error_rate = 1 - modle_accuracy;
model_confusion = zeros(7);
for i = 1:size(model_yfit,1)
    actual_string = string(table2array(test_data(i,end)));
    actual_num = stringAsRound(actual_string);
    guess_string = string(model_yfit(i));
    guess_num = stringAsRound(guess_string);
    model_confusion(actual_num,guess_num) = model_confusion(actual_num,guess_num) + 1;
end
modle_accuracy
model_error_rate
model_confusion

function round = stringAsRound(class)
    if class == "C"
        round = 1;
    elseif class == "CG"
        round = 2;
    elseif class == "FF"
        round = 3;
    elseif class == "E8"
        round = 4;
    elseif class == "S16"
        round = 5;
    elseif class == "R32"
        round = 6;
    elseif class == "R64"
        round = 7;
    end
end

% ensemble_sfs_yfit = ensemble_sfs_model.predictFcn(test_data);
% ensemble_sfs_accuracy = sum(ensemble_sfs_yfit==table2array(test_data(:,end)))/size(ensemble_sfs_yfit,1);
% ensemble_sfs_error_rate = 1 - ensemble_sfs_accuracy;
% ensemble_sfs_confusion = zeros(7);
% for i = 1:size(ensemble_sfs_yfit,1)
%     actual = table2array(test_data(i,end));
%     guess = ensemble_sfs_yfit(i);
%     ensemble_sfs_confusion(actual,guess) = ensemble_sfs_confusion(actual,guess) + 1;
% end
% 
% knn_pca_yfit = knn_pca_model.predictFcn(test_data);
% knn_pca_accuracy = sum(knn_pca_yfit==table2array(test_data(:,end)))/size(knn_pca_yfit,1);
% knn_pca_error_rate = 1 - knn_pca_accuracy;
% knn_pca_confusion = zeros(7);
% for i = 1:size(knn_pca_yfit,1)
%     actual = table2array(test_data(i,end));
%     guess = knn_pca_yfit(i);
%     knn_pca_confusion(actual,guess) = knn_pca_confusion(actual,guess) + 1;
% end
% 
% knn_sfs_yfit = knn_sfs_model.predictFcn(test_data);
% knn_sfs_accuracy = sum(knn_sfs_yfit==table2array(test_data(:,end)))/size(knn_sfs_yfit,1);
% knn_sfs_error_rate = 1 - knn_sfs_accuracy;
% knn_sfs_confusion = zeros(7);
% for i = 1:size(knn_sfs_yfit,1)
%     actual = table2array(test_data(i,end));
%     guess = knn_sfs_yfit(i);
%     knn_sfs_confusion(actual,guess) = knn_sfs_confusion(actual,guess) + 1;
% end
% 
% svm_pca_yfit = svm_pca_model.predictFcn(test_data);
% svm_pca_accuracy = sum(svm_pca_yfit==table2array(test_data(:,end)))/size(svm_pca_yfit,1);
% svm_pca_error_rate = 1 - svm_pca_accuracy;
% svm_pca_confusion = zeros(7);
% for i = 1:size(svm_pca_yfit,1)
%     actual = table2array(test_data(i,end));
%     guess = svm_pca_yfit(i);
%     svm_pca_confusion(actual,guess) = svm_pca_confusion(actual,guess) + 1;
% end
% 
% svm_sfs_yfit = svm_sfs_model.predictFcn(test_data);
% svm_sfs_accuracy = sum(svm_sfs_yfit==table2array(test_data(:,end)))/size(svm_sfs_yfit,1);
% svm_sfs_error_rate = 1 - svm_sfs_accuracy;
% svm_sfs_confusion = zeros(7);
% for i = 1:size(svm_sfs_yfit,1)
%     actual = table2array(test_data(i,end));
%     guess = svm_sfs_yfit(i);
%     svm_sfs_confusion(actual,guess) = svm_sfs_confusion(actual,guess) + 1;
% end
