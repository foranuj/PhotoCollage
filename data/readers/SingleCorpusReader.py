from yearbook.Corpus import Corpus
from yearbook.Photograph import Photograph


def single_corpus_processor(corpus_file) -> {}:
    face_to_image_map = {}
    event_to_image_map = {}  # For a given event, we can track the images

    all_images_map = {}

    # read the corpus file
    with open(corpus_file, 'r') as reader:
        for line in reader.readlines():
            values = line.split("\t")
            event_name = values[0]
            img_name = values[1].strip()

            photograph = Photograph(img_name, [], event_name)

            if event_name in event_to_image_map:
                event_to_image_map[event_name].append(img_name)
            else:
                event_to_image_map[event_name] = [img_name]

            all_images_map[photograph.name] = photograph

    return Corpus(image_map=all_images_map, events_to_images=event_to_image_map)
