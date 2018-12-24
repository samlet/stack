class CustomFormAction(FormAction):
    def name(self):
        return "${form_name}_form"

    @staticmethod
    def required_slots(_tracker):
        return ${str(slots)}

