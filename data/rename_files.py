import os
os.getcwd()
collection = "C:/Python/lightweight/data/01_luke_premium"
for i, filename in enumerate(os.listdir(collection)):
    os.rename("C:/Python/lightweight/data/01_luke_premium/" + filename,
              "C:/Python/lightweight/data/01_luke_premium/" + "01_luke_premium" + filename)