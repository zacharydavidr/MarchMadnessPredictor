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
