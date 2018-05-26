function [z,w,v,error_train,error_val] = mlptrain(train_data_txt,val_data_txt, m, k)
%Multilayer perceptron (neural network) for classification. Uses ReLU
%activation function.
%Hidden units returned are for the training data. m hidden units, k classes

%Check if using combined data or not
try
    train_data = importdata(train_data_txt);
    val_data = importdata(val_data_txt);
    [n_val,d] = size(val_data);
    combined = false;
catch
    train_data = train_data_txt;
    [~,d] = size(train_data);
    val_data = ones(1,d);
    combined = true;
    n_val = 1;
end

%number of variables maintained at d since classifying column
%removed but ones column added
[n,~] = size(train_data);

%Add column of ones to train_data
X_train = ones(n,1);
X_train = [X_train, train_data(:,1:(d-1))];
X_val = ones(n_val,1);
X_val = [X_val, val_data(:,1:(d-1))];

%create r matrix for train and val data
r_train = zeros(n,k);
for t = 1:n
    r_train(t,(train_data(t,d)+1)) = 1;
end
r_val = zeros(n_val,k);
for t = 1:n_val
    r_val(t, (val_data(t,d)+1)) = 1;
end

%Initalize interval for random numbers
a = -.01;
b = .01;

%Initialize variables
w = a+(b-a)*rand(m,d); %d already includes +1 of constant term
v = a+(b-a)*rand(k,m + 1);
z = zeros(n,m+1);
z(:,m+1) = 1;
y = zeros(k,1);
stepsize = 5e-4;
delta_w = zeros(m,d);
delta_v = zeros(k,m+1);
predicted = zeros(n,1);

%Initialize variables for validation
z_val = zeros(n_val,m+1);
z_val(:,m+1)= 1;
y_val = zeros(k,1);
predicted_val = zeros(n_val,1);

%
break_val = .97;
dif = 0;
temp = 100;
hold_error = zeros(temp,1);
hold_error_val = zeros(temp,1);



%---------------------Begin Gradient Descent----------------------------
converged = false;
count = 0;
while converged ~= true
    
    %Increment count and reset variables
    count = count + 1;
    Error = 0;
    Error_val = 0;
    
    %need to randomize order
    observations = randperm(n);
    for obs = 1:n
        t = observations(obs);
        
        %----------set Z with ReLU, if less than 0 make zero---
        for h = 1:m
            z(t,h) = w(h,:)*X_train(t,:)';
            if z(t,h) < 0
                z(t,h) = 0;
            end
        end
        
        %------------------set y with softmax-------------------
        for i = 1:k
            hold_value = v(i,:)*z(t,:)';
            y(i) = exp(hold_value);
        end
        
        y = y./sum(y);
        
        %-------------------determine delta v-------------------
        for h = 1:(m+1)
            for i = 1:k
                delta_v(i,h) = stepsize*(r_train(t,i) - y(i))*z(t,h);
            end
        end
        
        %-------------------determine delta w--------------------
        for j = 1:d
            for h = 1:m
                %reset to zero so not altered incorrectly
                delta_w(h,j) = 0;
                %ReLU, under zero do not change
                if w(h,:)*X_train(t,:)' < 0
                    continue
                end
                
                for i = 1:k
                    delta_w(h,j) = delta_w(h,j) + (r_train(t,i) - y(i))*v(i,h);
                end
                
                delta_w(h,j) = stepsize*delta_w(h,j)*X_train(t,j);
            end
        end
        
        %---------------------change v,w-------------------------
        for h = 1:(m+1)
            for i = 1:k
                v(i,h) = v(i,h) + delta_v(i,h);
            end
            if h == m+1
                continue
            end
            for j = 1:d
                w(h,j) = w(h,j) + delta_w(h,j);
            end
        end
    
    %---------------------------miscellaneous---------------------  
        
        %sum error for this 'round'
        for i = 1:k
            Error = Error - r_train(t,i)*log(y(i)); 
        end
    end
    %used to plot error
    hold_error(count) = Error;
    
    %---------------determine convergence---------------
    check = randi(3,1);
    if (count > 7) && (check == 1)
        dif = mean(hold_error(count-3:count)) - mean(hold_error(count - 7: count - 4));
        dif = 1 +  dif/mean(hold_error(count-7:count-4));
        %Dropout point, else overfitting
        if Error < 5
            dif = 1;
        end
    end
    
    %----Add adaptive learning rate-----
    if (count > 1) && (hold_error(count) < hold_error(count-1))
        stepsize = stepsize + 1e-4;
    else
        stepsize = .9*stepsize;
    end
    
    
    %------------------------Validation---------------------------
    %Order no longer important
    for t = 1:n_val
        
                %------set z_val with ReLU-----
        for h = 1:m
            z_val(t,h) = w(h,:)*X_val(t,:)';
            if z_val(t,h) < 0
                z_val(t,h) = 0;
            end
        end
        
                %-----Set y with softmax------
        for i = 1:k
            hold_value = v(i,:)*z_val(t,:)';
            y_val(i) = exp(hold_value);
        end
        y_val = y_val./sum(y_val);
        

                %add error from each observation
        for i = 1:k
            Error_val = Error_val - r_val(t,i)*log(y_val(i));
        end 
    end
    
    %add total error_val
    hold_error_val(count) = Error_val;

    %Break condition
    if dif > break_val
        break
    end  
end
%--------------Gradient descent complete---------------


%----------Calculate Classification error on train & validation sets------
predicted_train = zeros(n,1);
predicted_val = zeros(n_val,1);
%%%%Recalculate Z
for t = 1:n  
    %Softmax classifier
    %----------set Z with ReLU, if less than 0 make zero---
    for h = 1:m
        z(t,h) = w(h,:)*X_train(t,:)';
        if z(t,h) < 0
           z(t,h) = 0;
        end
    end
    %set y's
    for i = 1:k
        y(i) = exp(v(i,:)*z(t,:)');
    end
    y = y./sum(y);
    
    %retrieve greatest value
    class = find(y == max(y)) -1;
    predicted_train(t) = class;
end
for t = 1:n_val
    for i = 1:k
        y(i)= exp(v(i,:)*z_val(t,:)');
    end
    y = y./sum(y);
    
    class = find(y == max(y)) -1;
    predicted_val(t) = class;
end
%Remove ones column
z = z(:,1:m);

%Classification error
error_train = 1 - mean(predicted_train == train_data(:,d)); 
error_val = 1 - mean(predicted_val == val_data(:,d));


%Print errors
sprintf('Classification error on training data for %i hidden units: %f',m,error_train)
if combined == false
    sprintf('Classification error on validation data for %i hidden units: %f',m, error_val)
end

sprintf('- Log likelihood value on training data for %i hidden units: %f',m,hold_error(count))
if combined == false
    sprintf('- Log likelihood value on validation data for %i hidden units: %f',m, hold_error_val(count))
end  

%{}
%--plots, not needed but nice to see if properly working or overfitting---
%Feel free to close out
figure
plot(1:count, hold_error(1:count))
hold on
if combined == false
    plot(1:count, hold_error_val(1:count), 'r')
end
xlabel('Epochs')
ylabel('-Log Likelihood')
ttl = sprintf('Error Function Value by Epochs, %i hidden units', m);
title(ttl);
if combined == false
    legend('Training Error', 'Validation Error');
else
    legend('Combined Training & Validation Error');
end
hold off
%}



