#Have fun with reconstructing images using different PCA loadings
#Load 4 images, two similar images and two different images named 'pic1.jpg' to 'pic4.jpg'.
#pic1 and pic3's eigen vectors will be used to re-create pic2 and pic4 respectively 
#(in addtion to themselves)
#pic1 and pic2 MUST be same pixel dimension and pic3 pic4 MUST be same pixel dimension.
#Reconstructing a decent image can very widely between pictures.

library(jpeg)

#program automaticall determines k (eigen vectors to use in image reconstruction) but if you
#want can change k and see results (Change OVERRIDE_k to value > 0)
OVERRIDE_k = 0

#Similar and different pictures. 
sim1 <- readJPEG('pic1.jpg')
sim2 <- readJPEG('pic2.jpg')
dif1 <- readJPEG('pic3.jpg')
dif2 <- readJPEG('pic4.jpg')

#check all the same size
if ((dim(sim1)[1] != dim(sim2)[1]) | (dim(sim1)[2] != dim(sim2)[2])){
  stop('Picture 1 and 2 are not the same dimension')
}
if ((dim(dif1)[1] != dim(dif1)[1]) | (dim(dif2)[2] != dim(sim2)[2])){
  stop('Picture 3 and 4 are not the same dimension')
}

#for loop to go through both sets of pictures. Loop changes img1 and img2
#in second itteration (to dif1 and dif2)
img1 = sim1
img2 = sim2
for(set in 1:2){
  #retrieve dimensions, n is obvervationds d is variables in each color
  hold = dim(img1)
  n = hold[1]
  d = hold[2]
  
  #break down by color componenets of matrix
  r1 <- img1[,,1]
  g1 <- img1[,,2]
  b1 <- img1[,,3]
  
  #second Image
  r2 <- img2[,,1]
  g2 <- img2[,,2]
  b2 <- img2[,,3]
  
  #Eigen decompositionon each color of image 1
  Eigs_r1 = eigen(cov(r1))
  Eigs_g1 = eigen(cov(g1))
  Eigs_b1 = eigen(cov(b1))
  
  #
  #Use variance explained to determine how many variables to use
  var_total_r1 = sum(Eigs_r1$values)
  var_total_g1 = sum(Eigs_g1$values)
  var_total_b1 = sum(Eigs_b1$values)
  
  var_perPC_r1 = Eigs_r1$values*(1/var_total_r1)
  var_perPC_g1 = Eigs_g1$values*(1/var_total_g1)
  var_perPC_b1 = Eigs_b1$values*(1/var_total_b1)
  
  #holds variance explained of all colors, each corresponding to a column. Used to decide on
  #How many eigen vectors to use in reconstruction
  r1_g1_b1 = matrix(c(var_perPC_r1,var_perPC_g1,var_perPC_b1), nrow = d, ncol = 3)
  
  #iterate through colors
  #Use k components that explain 99.5% of variance
  if(OVERRIDE_k == 0){
    explained = .995
    sum_k = 0
    for (col in 1:3) {
      
      #find appropiate choise of k componenets to use. Reset variables each iteration
      k = 0
      var_expl = 0
      while(var_expl < explained ){
        k = k + 1
        var_expl = var_expl + r1_g1_b1[k, col]
      }
      #sum all values of k to be 
      sum_k = sum_k + k
    }
    #take truncated average of k
    k = trunc(sum_k/3)
    print(sprintf('Use approximately %i components which explain %f of variance', k, explained))
  }
  
  else{
    #If override set, change k
    k = OVERRIDE_k
    print(sprintf('Use %i componenets',k))
    }
  
  #reconstruct image with specified number of eigen vectors. Rename for ease
  A_r = Eigs_r1$vectors[,1:k]
  A_g = Eigs_g1$vectors[,1:k]
  A_b = Eigs_b1$vectors[,1:k]
  
  recon_r1 = r1%*%A_r%*%t(A_r)
  recon_g1 = g1%*%A_g%*%t(A_g)
  recon_b1 = b1%*%A_b%*%t(A_b)
  
  #put together image
  recon_img = array(c(recon_r1,recon_g1,recon_b1),dim = c(n,d,3))
  
  #Write image to file
  name = sprintf('Reconstructed_1_%s_%s.jpg',set, k)
  writeJPEG(recon_img, name)
  
  recon_r2 = r2%*%(A_r)%*%t(A_r)
  recon_g2 = g2%*%(A_g)%*%t(A_g)
  recon_b2 = b2%*%(A_b)%*%t(A_b)
  
  recon_img_2 = array(c(recon_r2,recon_g2,recon_b2),dim = c(n,d,3))
  
  #Write image to file
  name = sprintf('Reconstructed_2_%s_%s.jpg',set, k)
  writeJPEG(recon_img_2, name)
  
  #set images for second iteration
  img1 = dif1
  img2 = dif2
}