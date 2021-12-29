def get_portrait_images_for_child(drive_dir, school_name, child):
    import os
    images_per_child = []

    try:
        selfie_dir = os.path.join(drive_dir, school_name, "Selfies", child)
        images_per_child = [os.path.join(selfie_dir, image) for image in os.listdir(selfie_dir)
                            if image.endswith("jpg")]
    except:
        pass

    return images_per_child


class Corpus:

    def __init__(self, school_name: str, image_map: {}, events_to_images: {}, child_to_images: {}, corpus_dir: str):
        self.school_name = school_name
        self.image_map = image_map
        self.events_to_images = events_to_images
        self.child_to_images = child_to_images
        self.corpus_dir = corpus_dir

    def get_children(self):
        return self.child_to_images.keys()

    def get_events(self):
        return self.events_to_images.keys()

    def is_image_from_event(self, image, event):
        # Doesn't check for missing events for now
        return image in self.events_to_images[event]

    def get_images_for_event(self, event):
        # Doesn't check for missing events for now
        return self.events_to_images[event]

    def get_filenames_for_event_images(self, event):
        import os
        images_per_event = self.events_to_images[event]
        return [os.path.join(self.corpus_dir, event, a_tuple) for a_tuple in images_per_event]

    def get_child_images_for_event(self, child, event):

        child_images_per_event = []
        childs_image_names = [image_tuple[0] for image_tuple in self.child_to_images[child]]

        for image in self.events_to_images[event]:
            if image in childs_image_names:
                child_images_per_event.append(image)

        return child_images_per_event

    def get_filenames_child_images_for_event(self, child, event):
        import os
        child_images_per_event = self.get_child_images_for_event_with_scores(child, event)

        # TODO: Figure out what should the fallback be in cases where there are no images of this child
        # in this event. For now we're returning everything from that event
        if len(child_images_per_event) < 2:
            child_images_per_event = self.events_to_images[event]
            return [os.path.join(self.corpus_dir, event, a_tuple) for a_tuple in child_images_per_event]

        return [os.path.join(self.corpus_dir, event, a_tuple[0]) for a_tuple in child_images_per_event]

    def get_child_images_for_event_with_scores(self, child, event):

        child_images_per_event = []
        try:
            for image in self.child_to_images[child]:
                if image[0] in self.events_to_images[event]:
                    child_images_per_event.append(image)
        except KeyError:
            # This means child doesn't have any images specific to this event
            # We should show all images in that case. And we provide a tuple with image_name, score, and bounding_box []
            [child_images_per_event.append((image, '0.5', [])) for image in self.events_to_images[event]]

        return child_images_per_event

    def get_images_with_face_count(self, face_count: int):

        return {k:v for k,v in self.image_map.items() if len(v.faces) == face_count}
