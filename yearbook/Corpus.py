class Corpus:

    def __init__(self, image_map: {}, events_to_images: {}):
        self.image_map = image_map
        self.events_to_images = events_to_images

    def get_children(self):
        return self.child_to_images.keys()

    def get_events(self):
        return self.events_to_images.keys()

    def is_image_from_event(self, image, event):
        return image in self.events_to_images[event]

    def get_child_images_for_event(self, event):
        return self.events_to_images[event]
