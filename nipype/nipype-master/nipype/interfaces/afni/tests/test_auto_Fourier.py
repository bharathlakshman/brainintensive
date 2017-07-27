# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import Fourier


def test_Fourier_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    highpass=dict(argstr='-highpass %f',
    mandatory=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='%s',
    copyfile=False,
    mandatory=True,
    position=-1,
    ),
    lowpass=dict(argstr='-lowpass %f',
    mandatory=True,
    ),
    out_file=dict(argstr='-prefix %s',
    name_source='in_file',
    name_template='%s_fourier',
    ),
    outputtype=dict(),
    retrend=dict(argstr='-retrend',
    ),
    terminal_output=dict(nohash=True,
    ),
    )
    inputs = Fourier.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_Fourier_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = Fourier.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value