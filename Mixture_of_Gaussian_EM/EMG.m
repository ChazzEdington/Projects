function [h,m, Q] = EMG(flag,image, k)
%Expectation maximization function. Needs Expected_Q.m function to run

%Check flag value
if flag ~= 0 
    if flag ~= 1
        error('Flag is not value 0 or 1')
    end
end

%load images
[img, cmap] = imread(image);
img_rgb = ind2rgb(img,cmap);
img_double = im2double(img_rgb);
%reshape
[n1,n2,d] = size(img_rgb);
N = n1*n2;
X = reshape(img_rgb, [N,d]);

%set lambda
lambda = .25*flag;

%When constructing new image, will be its name
img_name = sprintf('%s_EM%i_%i.bmp',image(1:end-4),flag,k);


%initialize variables
PI = repmat(1/k, k,1);
%m = rand(k,d); %set with k means
S = rand(d,d,k);
for i = 1:k
    S(:,:,i) = S(:,:,i)*S(:,:,i)' + eye(d); 
end
h = zeros(N,k);



warning('off');
[~,m] = kmeans(X,k,'MaxIter',2,'EmptyAction','singleton');
warning('on');

%if expected log likelihood changes less than converged, break out of loop
%if iterate more than break_value break out of loop. Break if under .7%change
change = 1;
converged = 6.5*10^(-3);
break_val = 100;
loops = 0;

Q = zeros(2*break_val, 1);
q_pos = 0;

%error messages
Ecov_err = ['Error in Expectation Step: Covariance matrix in singular, Gaussian '...
    'density cannot be applied'];
Mcov_err =['Error in Maximization Step: Covariance matrix in singular, Gaussian '...
    'density cannot be applied.'];

%begin EM
while change > converged
    
    %----------------------------Expectation step-----------------------------
    q_pos = q_pos +1;
    %determine h values
    for t = 1:N
        h_hold = 0;
        for i = 1:k       
            h(t,i) = PI(i)*mvnpdf(X(t,:)',m(i,:)',S(:,:,i));
            h_hold = h_hold + h(t,i);
        end
        h(t,:) = 1./(h_hold./h(t,:));
    end
    
    %assign expected complete log likelihood value
    try
        Q(q_pos) = Expected_Q(X,h,PI,m,S);
        
        %if improved em add term
        if flag ~=0
            if loops ==0
                val = 0;
                for i = 1:k
                    val = val+ sum(diag(inv(S(:,:,i))));
                end          
            end
            Q(q_pos) = Q(q_pos) - (lambda/2)*val;
        end
        
    catch
        error(Ecov_err)
    end
    %----------------------------Maximization step-----------------------------
    q_pos = q_pos +1;
    
    for i = 1:k
        
        PI(i) = sum(h(:,i))/N;
        m(i,:) = sum(h(:,i).*X)/sum(h(:,i));
        
        hold_var = 0;
        for t = 1:N
            hold_var = hold_var + h(t,i)*((X(t,:) - m(i,:))'*(X(t,:) - m(i,:)));
        end
        %improved expectation maximization, add lambda to diagonal 
        %(if flag == 1)
        hold_var = (hold_var + lambda*eye(d))/sum(h(:,i));
        S(:,:,i) = hold_var;
        
    end

    try
        Q(q_pos) = Expected_Q(X,h,PI,m,S);
        
        %if improved em add term
        if flag ~=0
            val = 0;
            for i = 1:k
                val = val+ sum(diag(inv(S(:,:,i))));
            end
                
            Q(q_pos) = Q(q_pos) - (lambda/2)*val;
        end  
                    
    catch
        error(Mcov_err)
    end
    
    %------------------------Various Other Things--------------------------   
    
    %determine change, do not look at until after 5 iterations. Allow start 
    %converging before attempting to break
    if q_pos > 10
        change = diff(Q((q_pos -2):2:q_pos))/abs(Q(q_pos - 2));
        
        %{
        %possible errors
        if isinf(change) == 1
            error('Absolute value of Q has gone to infinity')
        elseif isnan(change) == 1
            error('Q is NaN')
        elseif change < 0
            Q(1:q_pos)
            error('Maximization Step: Decreasing')
        end
        %}
    end
    
    %
    %Writes pic each step for if it fails
    idx = (h' == max(h'))';
    file_write = zeros(N,d);

    %assign to nearest neigbor
    for t = 1:N
        file_write(t,:) = m(idx(t,:),:)';
    end
    %write file
    file_write = reshape(file_write,[n1,n2,d]);
    imwrite(file_write,img_name)
    %}
    
    
    %Stop afters so many loops
    loops = loops + 1;
    if loops >= break_val
        break
    end
end

Q = Q(1:q_pos);
figure
plot(1:q_pos, Q)
xlabel('Step (2 Steps = 1 Iteration of EM)')
ylabel('Expected Complete Log Likelihood Value')
title(sprintf('Expected Complete Log Likelihood per Step for K = %i Clusters (flag = %i)',k,flag))
hold on
scatter(1:2:q_pos,Q(1:2:q_pos),'r','filled')
scatter(2:2:q_pos,Q(2:2:q_pos),'b','filled')
    
end

