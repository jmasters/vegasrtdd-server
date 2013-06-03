# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PBVegasData.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='PBVegasData.proto',
  package='',
  serialized_pb='\n\x11PBVegasData.proto\"\xca\x04\n\x0bpbVegasData\x12\x0c\n\x04\x64\x61ta\x18\x01 \x03(\x02\x12\x13\n\x0b\x63\x65nter_freq\x18\x02 \x03(\x01\x12\x11\n\tdata_dims\x18\x03 \x03(\x03\x12\x11\n\tcal_state\x18\x04 \x03(\x05\x12\x15\n\rsig_ref_state\x18\x05 \x03(\x05\x12\x18\n\x10integration_time\x18\x06 \x03(\x02\x12\x0c\n\x04time\x18\x14 \x01(\x01\x12\x14\n\x0ctime_counter\x18\x15 \x01(\x03\x12\x13\n\x0bintegration\x18\x16 \x01(\x03\x12\x10\n\x08\x65xposure\x18\x17 \x01(\x02\x12\x0e\n\x06object\x18\x18 \x01(\t\x12\x0f\n\x07\x61zimuth\x18\x19 \x01(\x02\x12\x11\n\televation\x18\x1a \x01(\x02\x12\x0c\n\x04\x62maj\x18\x1b \x01(\x02\x12\x0c\n\x04\x62min\x18\x1c \x01(\x02\x12\x0b\n\x03\x62pa\x18\x1d \x01(\x02\x12\x0f\n\x07\x61\x63\x63umid\x18\x1e \x01(\x03\x12\x0f\n\x07sttspec\x18\x1f \x01(\x03\x12\x0f\n\x07stpspec\x18  \x01(\x03\x12\x17\n\x0f\x63\x65nter_freq_idx\x18! \x01(\x02\x12\n\n\x02ra\x18\" \x01(\x01\x12\x0b\n\x03\x64\x65\x63\x18# \x01(\x01\x12\x10\n\x08\x64\x61ta_len\x18$ \x01(\x03\x12\x15\n\rnumber_phases\x18% \x01(\x03\x12\x16\n\x0enumber_spectra\x18& \x01(\x03\x12\x15\n\rnumber_stokes\x18\' \x01(\x03\x12\x14\n\x0cpolarization\x18( \x01(\t\x12\x17\n\x0fnumber_channels\x18) \x01(\x03\x12\x19\n\x11reference_channel\x18* \x01(\x02\x12\x12\n\nfpga_clock\x18+ \x01(\x02')




_PBVEGASDATA = _descriptor.Descriptor(
  name='pbVegasData',
  full_name='pbVegasData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='pbVegasData.data', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='center_freq', full_name='pbVegasData.center_freq', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data_dims', full_name='pbVegasData.data_dims', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cal_state', full_name='pbVegasData.cal_state', index=3,
      number=4, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sig_ref_state', full_name='pbVegasData.sig_ref_state', index=4,
      number=5, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='integration_time', full_name='pbVegasData.integration_time', index=5,
      number=6, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='pbVegasData.time', index=6,
      number=20, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_counter', full_name='pbVegasData.time_counter', index=7,
      number=21, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='integration', full_name='pbVegasData.integration', index=8,
      number=22, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exposure', full_name='pbVegasData.exposure', index=9,
      number=23, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object', full_name='pbVegasData.object', index=10,
      number=24, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='azimuth', full_name='pbVegasData.azimuth', index=11,
      number=25, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='elevation', full_name='pbVegasData.elevation', index=12,
      number=26, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bmaj', full_name='pbVegasData.bmaj', index=13,
      number=27, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bmin', full_name='pbVegasData.bmin', index=14,
      number=28, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bpa', full_name='pbVegasData.bpa', index=15,
      number=29, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='accumid', full_name='pbVegasData.accumid', index=16,
      number=30, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sttspec', full_name='pbVegasData.sttspec', index=17,
      number=31, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stpspec', full_name='pbVegasData.stpspec', index=18,
      number=32, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='center_freq_idx', full_name='pbVegasData.center_freq_idx', index=19,
      number=33, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ra', full_name='pbVegasData.ra', index=20,
      number=34, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dec', full_name='pbVegasData.dec', index=21,
      number=35, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data_len', full_name='pbVegasData.data_len', index=22,
      number=36, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='number_phases', full_name='pbVegasData.number_phases', index=23,
      number=37, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='number_spectra', full_name='pbVegasData.number_spectra', index=24,
      number=38, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='number_stokes', full_name='pbVegasData.number_stokes', index=25,
      number=39, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='polarization', full_name='pbVegasData.polarization', index=26,
      number=40, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='number_channels', full_name='pbVegasData.number_channels', index=27,
      number=41, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reference_channel', full_name='pbVegasData.reference_channel', index=28,
      number=42, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fpga_clock', full_name='pbVegasData.fpga_clock', index=29,
      number=43, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=22,
  serialized_end=608,
)

DESCRIPTOR.message_types_by_name['pbVegasData'] = _PBVEGASDATA

class pbVegasData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PBVEGASDATA

  # @@protoc_insertion_point(class_scope:pbVegasData)


# @@protoc_insertion_point(module_scope)