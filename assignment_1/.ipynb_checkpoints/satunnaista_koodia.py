#tässä oli tapa

# list of wanted columns
wanted_columns = ["age","blood pressure","specific gravity","albumin","sugar","blood glucose random","blood urea","sodium","potassium","hemoglobin","packed cell volume","white blood cell count","red blood cell count","class"]

# list of all columns and their abbreviations as a dict
columns = {
"age" : "age",
"blood pressure" : "bp",
"specific gravity" : "sg",
"albumin" : "al",
"sugar" : "su",
"red blood cells" : "rbc",
"pus cell" : "pc",
"pus cell clumps" : "pcc",
"bacteria" : "ba",
"blood glucose random" : "bgr",
"blood urea" : "bu",
"serum creatinine" : "sc",
"sodium" : "sod",
"potassium" : "pot",
"hemoglobin" : "hemo",
"packed cell volume" : "pcv",
"white blood cell count" : "wbcc",
"red blood cell count" : "rbcc",
"hypertension" : "htn",
"diabetes mellitus" : "dm",
"coronary artery disease" : "cad",
"appetite" : "appet",
"pedal edema" : "pe",
"anemia" : "ane",
"class" : "class"
}

# list of wanted abbreviations
wanted_abbreviations = [  columns[key]  for key in wanted_columns ]
print("Wanted abbreviations: ", wanted_abbreviations)

# units used
column_units = {


}


# columns and their abbreviations
columns_dictionary = {
"age" : "age",
"bp" : "blood pressure",
"sg" : "specific gravity",
"al" : "albumin",
"su" : "sugar",
"rbc" : "red blood cells",
"pc" : "pus cell",
"pcc" : "pus cell clumps",
"ba" : "bacteria",
"bgr" : "blood glucose random",
"bu" : "blood urea",
"sc" : "serum creatinine",
"sod" : "sodium",
"pot" : "potassium",
"hemo" : "hemoglobin",
"pcv" : "packed cell volume",
"wbcc" : "white blood cell count",
"rbcc" : "red blood cell count",
"htn" : "hypertension",
"dm" : "diabetes mellitus",
"cad" : "coronary artery disease",
"appet" : "appetite",
"pe" : "pedal edema",
"ane" : "anemia",
"class" : "class"
}