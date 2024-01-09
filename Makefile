
STATES := AL AK AZ AR CA CO CT DC DE FL \
		  GA HI ID IL IN IA KS KY LA ME \
		  MD MA MN MS MI MO MT NE NV NH \
		  NJ NM NY NC ND OH OK OR PA RI \
		  SC SD TN TX UT VT VA WA WV WI \
		  WY

LOG := INFO

RAW_DIR := ./raw
FARA_XLS := $(RAW_DIR)/FoodAccessResearchAtlasData2019.xlsx

DATASPECS := ./dataspecs
CENSUS_YAML := $(DATASPECS)/census2019.yaml

WORKING_DIR := ./working
FARA_CSV := $(WORKING_DIR)/fara.csv
CENSUS_DATA := $(STATES:%=$(WORKING_DIR)/census-%.csv)

DATASETS := $(STATES:%=$(WORKING_DIR)/faracen-%.csv)

.PHONY: all clean csv census datasets

all: datasets

clean:
	rm -rf $(WORKING_DIR)

csv: $(FARA_CSV)

census: $(CENSUS_DATA)

datasets: $(DATASETS)

$(FARA_CSV): $(FARA_XLS)
	mkdir -p $(@D)
	python -m faradata.faracsv --log $(LOG) -o $@ $<

$(WORKING_DIR)/census-%.csv: $(WORKING_DIR)/%.yaml
	censusdis download -o $@ $<

$(WORKING_DIR)/%.yaml: $(CENSUS_YAML)
	mkdir -p $(@D)
	sed 's/_STATE_/$(basename ${@F})/g' $< > $@

$(WORKING_DIR)/faracen-%.csv: $(WORKING_DIR)/census-%.csv $(FARA_CSV)
	python -m faradata.join --log $(LOG) --map $(WORKING_DIR)/map-$*.png --map-y lapophalf -o $@ $(WORKING_DIR)/census-$*.csv $(FARA_CSV)
