import os
county_list=['COARAPAHOE','CODENVER','MDANNEARUNDEL','MDBALTIMORE','MDMONTGOMERY','NJBURLINGTON','NJMONMOUTH','NJPASSAIC']
pkl_folder_list=['coarapahoe','codenver','mdannearundel','mdbaltimore','mdmontgomery','njburlington','njmonmouth','njpassaic']
# county_list=['COARAPAHOE','COCLEARCREEK','COCONEJOS','COCOSTILLA','CODELTA','CODENVER','CODOLORES','COELBERT','COGARFIELD','COGUNNISON','COLASANIMAS','COLOGAN','COMONTROSE','COOURAY','COPITKIN','COPROWERS','MDANNEARUNDEL','MDBALTIMORE','MDCALVERT','MDCECIL','MDCHARLES','MDDORCHESTER','MDFREDERICK','MDGARRETT','MDHARFORD','MDMONTGOMERY','MDQUEENANNES','MDWASHINGTON','MNWASHINGTON','NJBURLINGTON','NJCUMBERLAND','NJMERCER','NJMONMOUTH','NJPASSAIC','NJSALEM','NJWARREN','NYCAYUGA','NYCOLUMBIA','NYDUTCHESS','NYNIAGARA','NYONEIDA','NYORANGE','NYORLEANS','NYOSWEGO','NYSCHOHARIE','NYTOMPKINS','NYWASHINGTON','NYYATES']
# pkl_folder_list=['coarapahoe','coclearcreek','coconejos','cocostilla','codelta','codenver','codolores','coelbert','cogarfield','cogunnison','colasanimas','cologan','comontrose','coouray','copitkin','coprowers','mdannearundel','mdbaltimore','mdcalvert','mdcecil','mdcharles','mddorchester','mdfrederick','mdgarrett','mdharford','mdmontgomery','mdqueenannes','mdwashington','mnwashington','njburlington','njcumberland','njmercer','njmonmouth','njpassaic','njsalem','njwarren','nycayuga','nycolumbia','nydutchess','nyniagara','nyoneida','nyorange','nyorleans','nyoswego','nyschoharie','nytompkins','nywashington','nyyates']
print(county_list[0])
print(county_list.index(county_list[0]))
for index,county_name in enumerate(county_list):

  old_county = "county_list = ['NYYATES']"
  new_county = "county_list = ['" + str(county_name) + "']"

  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'r')
  filedata = f.read()
  f.close()


  newdata = filedata.replace(str(old_county),str(new_county))

  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'w')
  f.write(newdata)
  f.close()

  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'r')
  filedata = f.read()
  f.close()

  old_folder_path = "MyDrive/prodpkl/set2"
  # new_folder_path = "MyDrive/prodpkl/" + str(pkl_folder_list[index])
  new_folder_path = "MyDrive/pkls/countywisepkls/" + str(pkl_folder_list[index])

  newdata = filedata.replace(str(old_folder_path), str(new_folder_path))

  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'w')
  f.write(newdata)
  f.close()
# replaced with new
# now adding coounty name to file


  !python3 drive/MyDrive/tx_cts_prodpkl_collab.py  | grep Accuracy* >> /content/drive/MyDrive/AccuracyForProds.txt
# replaced with nyyates
  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'r')
  filedata = f.read()
  f.close()

  with open("/content/drive/MyDrive/AccuracyForProds.txt", 'a') as f:
    f.write("County Name = " + str(county_name))
    f.write(" : PKL Folder Name = " + str(new_folder_path) + " \n")
    f.close()


  newdata = filedata.replace(str(new_county),str(old_county))

  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'w')
  f.write(newdata)
  f.close()

  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'r')
  filedata = f.read()
  f.close()

  newdata = filedata.replace(str(new_folder_path), str(old_folder_path))

  f = open("/content/drive/MyDrive/tx_cts_prodpkl_collab.py",'w')
  f.write(newdata)
  f.close()
