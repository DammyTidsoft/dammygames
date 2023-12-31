## Models Schemas ###

### users/models.py ###


#### User ####
- id: int
- name: string
- password: string
- is_active: boolean
- mkanid: string
- is_staff: boolean
- last_login: datetime
- user_details: JSON(as gotten from tajnid API)

##### LoginAuditModel #####
- id: int
- user: User
- login_time: datetime
- logging_user: str (mkanid of user who logged in)
- logging_name: str (name of user who logged in)
- logging_success: boolean
- message (optional): str


### api/models.py ###

#### AbstractBaseModel ####
- created_at: datetime
- updated_at: datetime
- active: boolean
- 

#### Entity(AbstractBaseModel) ####
- id: int
- name: string
- description: string
- slug: string
- owners: User[]


#### Attribute(AbstractBaseModel) ####
- id: int
- name: string
- description: string
- slug: string
- entity: Entity
- points: int
- required: boolean
- data_type: string


#### Value(AbstractBaseModel) ####
- id: int
- attribute: Attribute
- entity: Entity
- uuid: string
- submitted_by: string
- submitted_for: string
- value: string
- submission_type: string
- month: int
- year: int
- user: User
- value_str: string
- value_int: int
- value_float: float
- value_bool: boolean
- value_date: datetime
- value_datetime: datetime
- value_time: datetime
- value_json: JSON

