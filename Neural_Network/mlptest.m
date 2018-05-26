function [z] = mlptest(test_data_txt, w, v)
%pass path to test data, w: matrix input unit weights, 
%v: hidden unit weights. Return hidden unit values

try
    data = importdata(test_data_txt);
    data_passed = 'test';
catch
    data = test_data_txt;
    data_passed = 'combined';
end
    
[n,d] = size(data);

%Data matrix which will be used
X = ones(n,1);
X = [X, data(:,1:(d-1))];

%initialize variables for MLP
[k,m] = size(v);
m = m-1;
z = zeros(n,m+1);
z(:,m+1) = 1;
y = zeros(k,1);

%initalize other variables
prediction = zeros(n,1);

%----------------------classify-------------------------
for t = 1:n
    
    %Set z with ReLU
    for h = 1:m
        z(t,h) = w(h,:)*X(t,:)';
        if z(t,h) < 0
            z(t,h) = 0;
        end
    end
    
    %Set y with soft max
    for i = 1:k
        y(i) = exp(v(i,:)*z(t,:)');
    end
    y = y./sum(y);
    
    %set prediction
    class = find(y == max(y)) - 1;
    prediction(t) = class;
end
%Remove ones column
z = z(:,1:m);
error = 1 - mean(prediction == data(:,d));
sprintf('Classification error on %s data: %f', data_passed,error)
            
    
    
