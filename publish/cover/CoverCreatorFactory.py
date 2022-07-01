from reportlab.lib.units import inch


class CoverSettings:
    def get_page_size(self):
        pass

    def get_top_left_back_cover(self):
        return 0, 0

    def get_top_left_front_cover(self):
        pass

    def get_cover_img_dims(self):
        pass

    def get_title_corner(self):
        pass


class HardCoverSettings(CoverSettings):

    def get_page_size(self):
        return 19 * inch, 12.75 * inch

    def get_cover_img_dims(self):
        width = 9.625 * inch
        height = 12.75 * inch
        return width, height

    def get_top_left_front_cover(self):
        x = 9.625 * inch
        y = 0. * inch
        return x, y

    def get_title_corner(self):
        return 14.5 * inch, 10 * inch


class SoftCoverSettings(CoverSettings):
    def get_page_size(self):
        return 17.38 * inch, 11.25 * inch

    def get_cover_img_dims(self):
        width = 8.69 * inch
        height = 11.25 * inch
        return width, height

    def get_top_left_front_cover(self):
        x = 8.69 * inch
        y = 0
        return x, y

    def get_top_left_back_cover(self):
        return 0, 0

    def get_title_corner(self):
        return 13.5 * inch, 9.25 * inch


class OnePageFrontHardCover(CoverSettings):
    def get_top_left_front_cover(self):
        x = 0
        y = 0
        return x, y

    def get_cover_img_dims(self):
        width = 8.75 * inch
        height = 11.25 * inch
        return width, height

    def get_page_size(self):
        return self.get_cover_img_dims()

    def get_top_left_back_cover(self):
        return 0, 0

    def get_title_corner(self):
        return 1.5 * inch, 9.25 * inch


def get_cover_settings(cover_format: str) -> CoverSettings:
    if cover_format.startswith("HardCover") or cover_format.startswith("Hardcover") or cover_format.startswith(
            "hardcover"):
        return HardCoverSettings()
    elif cover_format.startswith("SoftCover") or cover_format.startswith("Softcover") or cover_format.startswith(
            "softcover"):
        return SoftCoverSettings()
    elif cover_format.startswith("Digital") or cover_format.startswith("digital"):
        return OnePageFrontHardCover()
    else:
        raise ValueError(cover_format)
