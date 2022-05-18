class OrderDetails:
    def __init__(self, wix_order_id: str, cover_format: str):
        self.wix_order_id = wix_order_id
        self.cover_format = cover_format
        self.interior_pdf_url = None
        self.cover_url = None
        self.lulu_job_id: str = None
        self.child: str = None

        if self.cover_format == "Hardcover" or self.cover_format == "hardcover":
            self.pod_package_id = "0850X1100FCPRECW080CW444GXX"
        elif self.cover_format == "Softcover" or self.cover_format == "softcover":
            self.pod_package_id = "0850X1100FCPREPB080CW444GXX"
        else:
            self.pod_package_id = None

    def get_lulu_line_item(self):
        data = """{
                                "title": "%s",
                                "pod_package_id": "%s",
                                "quantity": 1,
                                "interior": {
                                    "source_url": "%s"
                                },
                                "cover": {
                                    "source_url": "%s"
                                }
                            }
            """ % (self.wix_order_id + "_" + self.child, self.pod_package_id, self.interior_pdf_url, self.cover_url)

        return data
