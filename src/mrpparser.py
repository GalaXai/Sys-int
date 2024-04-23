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
            if object_name in all_objects:
                continue

            # Create a shallow copy of object_data to avoid modifying the input data
            object_data = object_data.copy()

            # Parse dependencies if any
            if len(object_data) > 5 and object_data[5]:
                dependencies = object_data[5]
                if isinstance(dependencies, str):
                    dependencies = dependencies.split(", ")
                
                resolved_dependencies = []
                for lower_level_name in dependencies:
                    if lower_level_name not in all_objects:
                        # Recursively create the dependent object
                        all_objects[lower_level_name] = MRP(lower_level_name, *data[lower_level_name])
                    resolved_dependencies.append(all_objects[lower_level_name])
                
                object_data[5] = resolved_dependencies
            
            # Create the current object
            new_object = MRP(object_name, *object_data)
            all_objects[object_name] = new_object

        return MRPParser.filter_top_level_objects(all_objects)
