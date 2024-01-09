

STATES := 01 02 04 05 06 08 09 11 10 12 \
		  13 15 16 17 18 19 20 21 22 23 \
		  24 25 27 28 26 29 30 31 32 33 \
		  34 35 36 37 38 39 40 41 42 44 \
		  45 46 47 48 49 50 51 53 54 55 \
		  56


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
