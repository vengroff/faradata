
LOG := INFO

RAW_DIR := ./raw
FARA_XLS := $(RAW_DIR)/FoodAccessResearchAtlasData2019.xlsx

DATASPECS := ./dataspecs
CENSUS_YAML := $(DATASPECS)/census2019.yaml

WORKING_DIR := ./working
FARA_CSV := $(WORKING_DIR)/fara.csv
CENSUS_DATA := $(WORKING_DIR)/census2019.csv

DATASET := $(WORKING_DIR)/faracen.csv

.PHONY: all clean csv census dataset

all: dataset

clean:
	rm -rf $(WORKING_DIR)

csv: $(FARA_CSV)

census: $(CENSUS_DATA)

dataset: $(DATASET)

$(FARA_CSV): $(FARA_XLS)
	mkdir -p $(@D)
	python -m faradata.faracsv --log $(LOG) -o $@ $<

$(CENSUS_DATA): $(CENSUS_YAML)
	mkdir -p $(@D)
	censusdis download -o $@ $<

$(DATASET): $(CENSUS_DATA) $(FARA_CSV)
	python -m faradata.join --log $(LOG) -o $@ $(CENSUS_DATA) $(FARA_CSV)
