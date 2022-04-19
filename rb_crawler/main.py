from extract_rb import ExtractRb

if __name__ == "__main__":
    rb_id = 367482  # bakdata
    # rb_id = 368066

    rb = ExtractRb(rb_id, "be")
    corporate = rb.extract()
