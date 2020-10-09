function [Q] = Expected_Q(X,h,PI, m,S)
%calculate expected complete log likelihood value WITHOUT Regularization 
%term. Done seperately to keep EMG clean, regularization term added in
%EMG.m

Q = 0;
[N,k] = size(h);

for t = 1:N
    for i = 1:k
       
        try
            density = mvnpdf(X(t,:)',m(i,:)', S(:,:,i));
        catch
            error()
        end       
        %
        %prevent NaN and Inf
        if PI(i) == 0
            PI(i) = realmin;
        end
        if density == 0
            density = realmin;
        end      
         %}        
        Q = Q + h(t,i)*(log(PI(i)) + log(density));       
    end
end
end

