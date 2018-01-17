##########################################################################
#Develop the grand staff
##########################################################################

    
#Function to find keys from values            
def findKey(mydict,value):
    return [ key for key,val in mydict.items() if val==value ][0]
  
