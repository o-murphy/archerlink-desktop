from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OkStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_OK_STATUS: _ClassVar[OkStatusCode]
    SUCCESS: _ClassVar[OkStatusCode]

class ErrorStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ERROR_STATUS: _ClassVar[ErrorStatusCode]
    FAILURE: _ClassVar[ErrorStatusCode]
    INVALID_DATA: _ClassVar[ErrorStatusCode]

class HoldoffType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED: _ClassVar[HoldoffType]
    MIL: _ClassVar[HoldoffType]
    MOA: _ClassVar[HoldoffType]
    CLICKS: _ClassVar[HoldoffType]

class ColorScheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_COLOR_SHEME: _ClassVar[ColorScheme]
    SEPIA: _ClassVar[ColorScheme]
    BLACK_HOT: _ClassVar[ColorScheme]
    WHITE_HOT: _ClassVar[ColorScheme]

class AGCMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_AGC_MODE: _ClassVar[AGCMode]
    AUTO_1: _ClassVar[AGCMode]
    AUTO_2: _ClassVar[AGCMode]
    AUTO_3: _ClassVar[AGCMode]

class Zoom(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_ZOOM_LEVEL: _ClassVar[Zoom]
    ZOOM_X1: _ClassVar[Zoom]
    ZOOM_X2: _ClassVar[Zoom]
    ZOOM_X3: _ClassVar[Zoom]
    ZOOM_X4: _ClassVar[Zoom]
    ZOOM_X6: _ClassVar[Zoom]

class ButtonEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_BUTTON: _ClassVar[ButtonEnum]
    MENU_SHORT: _ClassVar[ButtonEnum]
    MENU_LONG: _ClassVar[ButtonEnum]
    UP_SHORT: _ClassVar[ButtonEnum]
    UP_LONG: _ClassVar[ButtonEnum]
    DOWN_SHORT: _ClassVar[ButtonEnum]
    DOWN_LONG: _ClassVar[ButtonEnum]
    LRF_SHORT: _ClassVar[ButtonEnum]
    LRF_LONG: _ClassVar[ButtonEnum]
    REC_SHORT: _ClassVar[ButtonEnum]
    REC_LONG: _ClassVar[ButtonEnum]

class CMDDirect(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN_CMD_DIRECTION: _ClassVar[CMDDirect]
    CALIBRATE_ACCEL_GYRO: _ClassVar[CMDDirect]
    LRF_MEASUREMENT: _ClassVar[CMDDirect]
    RESET_CM_CLICKS: _ClassVar[CMDDirect]
    TRIGGER_FFC: _ClassVar[CMDDirect]

class DType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VALUE: _ClassVar[DType]
    INDEX: _ClassVar[DType]

class GType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    G1: _ClassVar[GType]
    G7: _ClassVar[GType]
    CUSTOM: _ClassVar[GType]

class TwistDir(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RIGHT: _ClassVar[TwistDir]
    LEFT: _ClassVar[TwistDir]
UNKNOWN_OK_STATUS: OkStatusCode
SUCCESS: OkStatusCode
UNKNOWN_ERROR_STATUS: ErrorStatusCode
FAILURE: ErrorStatusCode
INVALID_DATA: ErrorStatusCode
UNDEFINED: HoldoffType
MIL: HoldoffType
MOA: HoldoffType
CLICKS: HoldoffType
UNKNOWN_COLOR_SHEME: ColorScheme
SEPIA: ColorScheme
BLACK_HOT: ColorScheme
WHITE_HOT: ColorScheme
UNKNOWN_AGC_MODE: AGCMode
AUTO_1: AGCMode
AUTO_2: AGCMode
AUTO_3: AGCMode
UNKNOWN_ZOOM_LEVEL: Zoom
ZOOM_X1: Zoom
ZOOM_X2: Zoom
ZOOM_X3: Zoom
ZOOM_X4: Zoom
ZOOM_X6: Zoom
UNKNOWN_BUTTON: ButtonEnum
MENU_SHORT: ButtonEnum
MENU_LONG: ButtonEnum
UP_SHORT: ButtonEnum
UP_LONG: ButtonEnum
DOWN_SHORT: ButtonEnum
DOWN_LONG: ButtonEnum
LRF_SHORT: ButtonEnum
LRF_LONG: ButtonEnum
REC_SHORT: ButtonEnum
REC_LONG: ButtonEnum
UNKNOWN_CMD_DIRECTION: CMDDirect
CALIBRATE_ACCEL_GYRO: CMDDirect
LRF_MEASUREMENT: CMDDirect
RESET_CM_CLICKS: CMDDirect
TRIGGER_FFC: CMDDirect
VALUE: DType
INDEX: DType
G1: GType
G7: GType
CUSTOM: GType
RIGHT: TwistDir
LEFT: TwistDir

class HostPayload(_message.Message):
    __slots__ = ("profile", "devStatus", "response", "reticles", "allProfiles")
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    DEVSTATUS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    RETICLES_FIELD_NUMBER: _ClassVar[int]
    ALLPROFILES_FIELD_NUMBER: _ClassVar[int]
    profile: HostProfile
    devStatus: HostDevStatus
    response: CommandResponse
    reticles: Reticles
    allProfiles: FullProfileData
    def __init__(self, profile: _Optional[_Union[HostProfile, _Mapping]] = ..., devStatus: _Optional[_Union[HostDevStatus, _Mapping]] = ..., response: _Optional[_Union[CommandResponse, _Mapping]] = ..., reticles: _Optional[_Union[Reticles, _Mapping]] = ..., allProfiles: _Optional[_Union[FullProfileData, _Mapping]] = ...) -> None: ...

class ClientPayload(_message.Message):
    __slots__ = ("devStatus", "command", "response")
    DEVSTATUS_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    devStatus: ClientDevStatus
    command: Command
    response: CommandResponse
    def __init__(self, devStatus: _Optional[_Union[ClientDevStatus, _Mapping]] = ..., command: _Optional[_Union[Command, _Mapping]] = ..., response: _Optional[_Union[CommandResponse, _Mapping]] = ...) -> None: ...

class CommandResponse(_message.Message):
    __slots__ = ("statusOk", "statusErr")
    STATUSOK_FIELD_NUMBER: _ClassVar[int]
    STATUSERR_FIELD_NUMBER: _ClassVar[int]
    statusOk: StatusOk
    statusErr: StatusError
    def __init__(self, statusOk: _Optional[_Union[StatusOk, _Mapping]] = ..., statusErr: _Optional[_Union[StatusError, _Mapping]] = ...) -> None: ...

class Command(_message.Message):
    __slots__ = ("setZoom", "setPallette", "setAgc", "setDst", "setHoldoff", "setZeroing", "setMagOffset", "setAirTC", "setAirHum", "setAirPress", "setPowderTemp", "setWind", "buttonPress", "cmdTrigger", "getHostDevStatus", "getHostProfile", "getAllProfiles", "updateAllProfiles", "getReticles", "updateReticles")
    SETZOOM_FIELD_NUMBER: _ClassVar[int]
    SETPALLETTE_FIELD_NUMBER: _ClassVar[int]
    SETAGC_FIELD_NUMBER: _ClassVar[int]
    SETDST_FIELD_NUMBER: _ClassVar[int]
    SETHOLDOFF_FIELD_NUMBER: _ClassVar[int]
    SETZEROING_FIELD_NUMBER: _ClassVar[int]
    SETMAGOFFSET_FIELD_NUMBER: _ClassVar[int]
    SETAIRTC_FIELD_NUMBER: _ClassVar[int]
    SETAIRHUM_FIELD_NUMBER: _ClassVar[int]
    SETAIRPRESS_FIELD_NUMBER: _ClassVar[int]
    SETPOWDERTEMP_FIELD_NUMBER: _ClassVar[int]
    SETWIND_FIELD_NUMBER: _ClassVar[int]
    BUTTONPRESS_FIELD_NUMBER: _ClassVar[int]
    CMDTRIGGER_FIELD_NUMBER: _ClassVar[int]
    GETHOSTDEVSTATUS_FIELD_NUMBER: _ClassVar[int]
    GETHOSTPROFILE_FIELD_NUMBER: _ClassVar[int]
    GETALLPROFILES_FIELD_NUMBER: _ClassVar[int]
    UPDATEALLPROFILES_FIELD_NUMBER: _ClassVar[int]
    GETRETICLES_FIELD_NUMBER: _ClassVar[int]
    UPDATERETICLES_FIELD_NUMBER: _ClassVar[int]
    setZoom: SetZoomLevel
    setPallette: SetColorScheme
    setAgc: SetAgcMode
    setDst: SetDistance
    setHoldoff: SetHoldoff
    setZeroing: SetZeroing
    setMagOffset: SetCompassOffset
    setAirTC: SetAirTemp
    setAirHum: SetAirHumidity
    setAirPress: SetAirPressure
    setPowderTemp: SetPowderTemp
    setWind: SetWind
    buttonPress: ButtonPress
    cmdTrigger: TriggerCmd
    getHostDevStatus: GetHostDevStatus
    getHostProfile: GetHostProfile
    getAllProfiles: GetProfiles
    updateAllProfiles: UpdateProfiles
    getReticles: GetReticles
    updateReticles: UpdateReticles
    def __init__(self, setZoom: _Optional[_Union[SetZoomLevel, _Mapping]] = ..., setPallette: _Optional[_Union[SetColorScheme, _Mapping]] = ..., setAgc: _Optional[_Union[SetAgcMode, _Mapping]] = ..., setDst: _Optional[_Union[SetDistance, _Mapping]] = ..., setHoldoff: _Optional[_Union[SetHoldoff, _Mapping]] = ..., setZeroing: _Optional[_Union[SetZeroing, _Mapping]] = ..., setMagOffset: _Optional[_Union[SetCompassOffset, _Mapping]] = ..., setAirTC: _Optional[_Union[SetAirTemp, _Mapping]] = ..., setAirHum: _Optional[_Union[SetAirHumidity, _Mapping]] = ..., setAirPress: _Optional[_Union[SetAirPressure, _Mapping]] = ..., setPowderTemp: _Optional[_Union[SetPowderTemp, _Mapping]] = ..., setWind: _Optional[_Union[SetWind, _Mapping]] = ..., buttonPress: _Optional[_Union[ButtonPress, _Mapping]] = ..., cmdTrigger: _Optional[_Union[TriggerCmd, _Mapping]] = ..., getHostDevStatus: _Optional[_Union[GetHostDevStatus, _Mapping]] = ..., getHostProfile: _Optional[_Union[GetHostProfile, _Mapping]] = ..., getAllProfiles: _Optional[_Union[GetProfiles, _Mapping]] = ..., updateAllProfiles: _Optional[_Union[UpdateProfiles, _Mapping]] = ..., getReticles: _Optional[_Union[GetReticles, _Mapping]] = ..., updateReticles: _Optional[_Union[UpdateReticles, _Mapping]] = ...) -> None: ...

class GetProfiles(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetReticles(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateReticles(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: Reticles
    def __init__(self, data: _Optional[_Union[Reticles, _Mapping]] = ...) -> None: ...

class UpdateProfiles(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: FullProfileData
    def __init__(self, data: _Optional[_Union[FullProfileData, _Mapping]] = ...) -> None: ...

class StatusOk(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: OkStatusCode
    def __init__(self, code: _Optional[_Union[OkStatusCode, str]] = ...) -> None: ...

class StatusError(_message.Message):
    __slots__ = ("code", "text")
    CODE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    code: ErrorStatusCode
    text: str
    def __init__(self, code: _Optional[_Union[ErrorStatusCode, str]] = ..., text: _Optional[str] = ...) -> None: ...

class SetZoomLevel(_message.Message):
    __slots__ = ("zoomLevel",)
    ZOOMLEVEL_FIELD_NUMBER: _ClassVar[int]
    zoomLevel: Zoom
    def __init__(self, zoomLevel: _Optional[_Union[Zoom, str]] = ...) -> None: ...

class SetColorScheme(_message.Message):
    __slots__ = ("scheme",)
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    scheme: ColorScheme
    def __init__(self, scheme: _Optional[_Union[ColorScheme, str]] = ...) -> None: ...

class GetHostDevStatus(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetHostProfile(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetAirTemp(_message.Message):
    __slots__ = ("temperature",)
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    temperature: int
    def __init__(self, temperature: _Optional[int] = ...) -> None: ...

class SetPowderTemp(_message.Message):
    __slots__ = ("temperature",)
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    temperature: int
    def __init__(self, temperature: _Optional[int] = ...) -> None: ...

class SetAirHumidity(_message.Message):
    __slots__ = ("humidity",)
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    humidity: int
    def __init__(self, humidity: _Optional[int] = ...) -> None: ...

class SetAirPressure(_message.Message):
    __slots__ = ("pressure",)
    PRESSURE_FIELD_NUMBER: _ClassVar[int]
    pressure: int
    def __init__(self, pressure: _Optional[int] = ...) -> None: ...

class SetWind(_message.Message):
    __slots__ = ("direction", "speed")
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    direction: int
    speed: int
    def __init__(self, direction: _Optional[int] = ..., speed: _Optional[int] = ...) -> None: ...

class SetDistance(_message.Message):
    __slots__ = ("distance",)
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    distance: int
    def __init__(self, distance: _Optional[int] = ...) -> None: ...

class SetAgcMode(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: AGCMode
    def __init__(self, mode: _Optional[_Union[AGCMode, str]] = ...) -> None: ...

class SetCompassOffset(_message.Message):
    __slots__ = ("offset",)
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    offset: int
    def __init__(self, offset: _Optional[int] = ...) -> None: ...

class SetHoldoff(_message.Message):
    __slots__ = ("x", "y", "type")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    type: HoldoffType
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., type: _Optional[_Union[HoldoffType, str]] = ...) -> None: ...

class ButtonPress(_message.Message):
    __slots__ = ("buttonPressed",)
    BUTTONPRESSED_FIELD_NUMBER: _ClassVar[int]
    buttonPressed: ButtonEnum
    def __init__(self, buttonPressed: _Optional[_Union[ButtonEnum, str]] = ...) -> None: ...

class TriggerCmd(_message.Message):
    __slots__ = ("cmd",)
    CMD_FIELD_NUMBER: _ClassVar[int]
    cmd: CMDDirect
    def __init__(self, cmd: _Optional[_Union[CMDDirect, str]] = ...) -> None: ...

class SetZeroing(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class HostDevStatus(_message.Message):
    __slots__ = ("charge", "zoom", "airTemp", "airHum", "airPress", "powderTemp", "windDir", "windSpeed", "pitch", "cant", "distance", "currentProfile", "colorScheme", "modAGC", "maxZoom")
    CHARGE_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    AIRTEMP_FIELD_NUMBER: _ClassVar[int]
    AIRHUM_FIELD_NUMBER: _ClassVar[int]
    AIRPRESS_FIELD_NUMBER: _ClassVar[int]
    POWDERTEMP_FIELD_NUMBER: _ClassVar[int]
    WINDDIR_FIELD_NUMBER: _ClassVar[int]
    WINDSPEED_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    CANT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    CURRENTPROFILE_FIELD_NUMBER: _ClassVar[int]
    COLORSCHEME_FIELD_NUMBER: _ClassVar[int]
    MODAGC_FIELD_NUMBER: _ClassVar[int]
    MAXZOOM_FIELD_NUMBER: _ClassVar[int]
    charge: int
    zoom: Zoom
    airTemp: int
    airHum: int
    airPress: int
    powderTemp: int
    windDir: int
    windSpeed: int
    pitch: int
    cant: int
    distance: int
    currentProfile: int
    colorScheme: ColorScheme
    modAGC: AGCMode
    maxZoom: Zoom
    def __init__(self, charge: _Optional[int] = ..., zoom: _Optional[_Union[Zoom, str]] = ..., airTemp: _Optional[int] = ..., airHum: _Optional[int] = ..., airPress: _Optional[int] = ..., powderTemp: _Optional[int] = ..., windDir: _Optional[int] = ..., windSpeed: _Optional[int] = ..., pitch: _Optional[int] = ..., cant: _Optional[int] = ..., distance: _Optional[int] = ..., currentProfile: _Optional[int] = ..., colorScheme: _Optional[_Union[ColorScheme, str]] = ..., modAGC: _Optional[_Union[AGCMode, str]] = ..., maxZoom: _Optional[_Union[Zoom, str]] = ...) -> None: ...

class ClientDevStatus(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CoefRow(_message.Message):
    __slots__ = ("bc_cd", "mv")
    BC_CD_FIELD_NUMBER: _ClassVar[int]
    MV_FIELD_NUMBER: _ClassVar[int]
    bc_cd: int
    mv: int
    def __init__(self, bc_cd: _Optional[int] = ..., mv: _Optional[int] = ...) -> None: ...

class SwPos(_message.Message):
    __slots__ = ("c_idx", "reticle_idx", "zoom", "distance", "distance_from")
    C_IDX_FIELD_NUMBER: _ClassVar[int]
    RETICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FROM_FIELD_NUMBER: _ClassVar[int]
    c_idx: int
    reticle_idx: int
    zoom: int
    distance: int
    distance_from: DType
    def __init__(self, c_idx: _Optional[int] = ..., reticle_idx: _Optional[int] = ..., zoom: _Optional[int] = ..., distance: _Optional[int] = ..., distance_from: _Optional[_Union[DType, str]] = ...) -> None: ...

class HostProfile(_message.Message):
    __slots__ = ("profile_name", "cartridge_name", "bullet_name", "short_name_top", "short_name_bot", "user_note", "zero_x", "zero_y", "sc_height", "r_twist", "c_muzzle_velocity", "c_zero_temperature", "c_t_coeff", "c_zero_distance_idx", "c_zero_air_temperature", "c_zero_air_pressure", "c_zero_air_humidity", "c_zero_w_pitch", "c_zero_p_temperature", "b_diameter", "b_weight", "b_length", "twist_dir", "bc_type", "switches", "distances", "coef_rows", "caliber", "device_uuid")
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CARTRIDGE_NAME_FIELD_NUMBER: _ClassVar[int]
    BULLET_NAME_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_TOP_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_BOT_FIELD_NUMBER: _ClassVar[int]
    USER_NOTE_FIELD_NUMBER: _ClassVar[int]
    ZERO_X_FIELD_NUMBER: _ClassVar[int]
    ZERO_Y_FIELD_NUMBER: _ClassVar[int]
    SC_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    R_TWIST_FIELD_NUMBER: _ClassVar[int]
    C_MUZZLE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    C_ZERO_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    C_T_COEFF_FIELD_NUMBER: _ClassVar[int]
    C_ZERO_DISTANCE_IDX_FIELD_NUMBER: _ClassVar[int]
    C_ZERO_AIR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    C_ZERO_AIR_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    C_ZERO_AIR_HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    C_ZERO_W_PITCH_FIELD_NUMBER: _ClassVar[int]
    C_ZERO_P_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    B_DIAMETER_FIELD_NUMBER: _ClassVar[int]
    B_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    B_LENGTH_FIELD_NUMBER: _ClassVar[int]
    TWIST_DIR_FIELD_NUMBER: _ClassVar[int]
    BC_TYPE_FIELD_NUMBER: _ClassVar[int]
    SWITCHES_FIELD_NUMBER: _ClassVar[int]
    DISTANCES_FIELD_NUMBER: _ClassVar[int]
    COEF_ROWS_FIELD_NUMBER: _ClassVar[int]
    CALIBER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_UUID_FIELD_NUMBER: _ClassVar[int]
    profile_name: str
    cartridge_name: str
    bullet_name: str
    short_name_top: str
    short_name_bot: str
    user_note: str
    zero_x: int
    zero_y: int
    sc_height: int
    r_twist: int
    c_muzzle_velocity: int
    c_zero_temperature: int
    c_t_coeff: int
    c_zero_distance_idx: int
    c_zero_air_temperature: int
    c_zero_air_pressure: int
    c_zero_air_humidity: int
    c_zero_w_pitch: int
    c_zero_p_temperature: int
    b_diameter: int
    b_weight: int
    b_length: int
    twist_dir: TwistDir
    bc_type: GType
    switches: _containers.RepeatedCompositeFieldContainer[SwPos]
    distances: _containers.RepeatedScalarFieldContainer[int]
    coef_rows: _containers.RepeatedCompositeFieldContainer[CoefRow]
    caliber: str
    device_uuid: str
    def __init__(self, profile_name: _Optional[str] = ..., cartridge_name: _Optional[str] = ..., bullet_name: _Optional[str] = ..., short_name_top: _Optional[str] = ..., short_name_bot: _Optional[str] = ..., user_note: _Optional[str] = ..., zero_x: _Optional[int] = ..., zero_y: _Optional[int] = ..., sc_height: _Optional[int] = ..., r_twist: _Optional[int] = ..., c_muzzle_velocity: _Optional[int] = ..., c_zero_temperature: _Optional[int] = ..., c_t_coeff: _Optional[int] = ..., c_zero_distance_idx: _Optional[int] = ..., c_zero_air_temperature: _Optional[int] = ..., c_zero_air_pressure: _Optional[int] = ..., c_zero_air_humidity: _Optional[int] = ..., c_zero_w_pitch: _Optional[int] = ..., c_zero_p_temperature: _Optional[int] = ..., b_diameter: _Optional[int] = ..., b_weight: _Optional[int] = ..., b_length: _Optional[int] = ..., twist_dir: _Optional[_Union[TwistDir, str]] = ..., bc_type: _Optional[_Union[GType, str]] = ..., switches: _Optional[_Iterable[_Union[SwPos, _Mapping]]] = ..., distances: _Optional[_Iterable[int]] = ..., coef_rows: _Optional[_Iterable[_Union[CoefRow, _Mapping]]] = ..., caliber: _Optional[str] = ..., device_uuid: _Optional[str] = ...) -> None: ...

class ProfileList(_message.Message):
    __slots__ = ("profile_desc", "activeprofile")
    PROFILE_DESC_FIELD_NUMBER: _ClassVar[int]
    ACTIVEPROFILE_FIELD_NUMBER: _ClassVar[int]
    profile_desc: _containers.RepeatedCompositeFieldContainer[ProfileListEntry]
    activeprofile: int
    def __init__(self, profile_desc: _Optional[_Iterable[_Union[ProfileListEntry, _Mapping]]] = ..., activeprofile: _Optional[int] = ...) -> None: ...

class ProfileListEntry(_message.Message):
    __slots__ = ("profile_name", "cartridge_name", "short_name_top", "short_name_bot", "file_path")
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CARTRIDGE_NAME_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_TOP_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_BOT_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    profile_name: str
    cartridge_name: str
    short_name_top: str
    short_name_bot: str
    file_path: str
    def __init__(self, profile_name: _Optional[str] = ..., cartridge_name: _Optional[str] = ..., short_name_top: _Optional[str] = ..., short_name_bot: _Optional[str] = ..., file_path: _Optional[str] = ...) -> None: ...

class FullProfileData(_message.Message):
    __slots__ = ("table", "profiles")
    TABLE_FIELD_NUMBER: _ClassVar[int]
    PROFILES_FIELD_NUMBER: _ClassVar[int]
    table: ProfileList
    profiles: _containers.RepeatedCompositeFieldContainer[HostProfile]
    def __init__(self, table: _Optional[_Union[ProfileList, _Mapping]] = ..., profiles: _Optional[_Iterable[_Union[HostProfile, _Mapping]]] = ...) -> None: ...

class Reticle(_message.Message):
    __slots__ = ("data", "folder_name")
    DATA_FIELD_NUMBER: _ClassVar[int]
    FOLDER_NAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    folder_name: str
    def __init__(self, data: _Optional[bytes] = ..., folder_name: _Optional[str] = ...) -> None: ...

class Reticles(_message.Message):
    __slots__ = ("rets",)
    RETS_FIELD_NUMBER: _ClassVar[int]
    rets: _containers.RepeatedCompositeFieldContainer[Reticle]
    def __init__(self, rets: _Optional[_Iterable[_Union[Reticle, _Mapping]]] = ...) -> None: ...

class Payload(_message.Message):
    __slots__ = ("profile",)
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    profile: HostProfile
    def __init__(self, profile: _Optional[_Union[HostProfile, _Mapping]] = ...) -> None: ...
