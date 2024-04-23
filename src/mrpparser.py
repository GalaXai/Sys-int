from .mrp import MRP

class MRPParser:
    @staticmethod
    def filter_top_level_objects(all_objects: dict[str, MRP]) -> list[MRP]:
        """
        Filters objects to return only the top-level objects.
        If an object is a lower-level object, it is removed.
        """
        objects_to_remove = []
        for obj in all_objects.values():
            for lower_level_obj in obj.mrp_array_lower_level:
                objects_to_remove.append(lower_level_obj.name)

        for obj_name in objects_to_remove:
            del all_objects[obj_name]

        return list(all_objects.values())

    @staticmethod
    def parse(data: dict) -> list[MRP]:
        all_objects = {}

        for object_name, object_data in data.items():
            # Check if the object has already been created
            if object_name in all_objects:
                continue

            # Check if the object has lower-level objects
            if len(object_data) > 5 and object_data[5]:
                if isinstance(object_data[5], str):
                    object_data[5] = object_data[5].split(", ")
                # Check if the lower-level objects have already been created
                for lower_level_name in object_data[5]:
                    if lower_level_name not in all_objects:
                        # Create the lower-level object
                        all_objects[lower_level_name] = MRP(lower_level_name, *data[lower_level_name])
                object_data[5] = [all_objects[obj_name] for obj_name in object_data[5]]
            
            new_object = MRP(object_name, *object_data)
            all_objects[new_object.name] = new_object

        return MRPParser.filter_top_level_objects(all_objects)