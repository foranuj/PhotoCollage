class Corpus:

    def __init__(self, image_map: {}, events_to_images: {}, child_to_images: {}):
        self.image_map = image_map
        self.events_to_images = events_to_images
        self.child_to_images = child_to_images

    def get_children(self):
        return self.child_to_images.keys()

    def get_events(self):
        return self.events_to_images.keys()

    def is_image_from_event(self, image, event):
        return image in self.events_to_images[event]

    def get_child_images_for_event(self, child, event):

        child_images_per_event = []
        childs_image_names = [image_tuple[0] for image_tuple in self.child_to_images[child]]

        for image in self.events_to_images[event]:
            if image in childs_image_names:
                child_images_per_event.append(image)

        return child_images_per_event

    def get_child_images_for_event_with_scores(self, child, event):

        child_images_per_event = []

        for image in self.child_to_images[child]:
            if image[0] in self.events_to_images[event]:
                child_images_per_event.append(image)

        return child_images_per_event

    def get_images_with_face_count(self, face_count: int):

        return {k:v for k,v in self.image_map.items() if len(v.faces) == face_count}
