import clusters
blognames,words,data=clusters.readfile('blogdata.txt')
rdata=clusters.rotatematrix(data)
wordclust=clusters.hcluster(rdata)
#clusters.printclust(clust,labels=blognames)
clusters.drawdendrogram(wordclust,labels=words,jpeg='wordclust.jpg')