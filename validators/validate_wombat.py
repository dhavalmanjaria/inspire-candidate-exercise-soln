from validators.dtos.validate_wombat_post_dto import ValidateWombatPostDTO


def validate_wombat_post(post_body_dict):
    if not 'name' in post_body_dict.keys():
        return ValidateWombatPostDTO(is_error=True, message='name')

    if not 'dob' in post_body_dict.keys():
        return ValidateWombatPostDTO(is_error=True, message='dob')

    return ValidateWombatPostDTO(is_error=False, message='')