IMAGES = data-model.svg

.phony: all

all: paper.pdf

paper.pdf: paper.md paper.bib $(IMAGES)
	sudo docker run --rm \
	    --volume ./:/data \
	    --user $(id -u):$(id -g) \
	    --env JOURNAL=joss \
	    openjournals/inara

data-model.svg: data-model.ditaa
	ditaa --svg $< $@
