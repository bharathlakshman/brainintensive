# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..resampling import ApplyTransformsToPoints


def test_ApplyTransformsToPoints_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    dimension=dict(argstr='--dimensionality %d',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    input_file=dict(argstr='--input %s',
    mandatory=True,
    ),
    invert_transform_flags=dict(),
    num_threads=dict(nohash=True,
    usedefault=True,
    ),
    output_file=dict(argstr='--output %s',
    hash_files=False,
    name_source=['input_file'],
    name_template='%s_transformed.csv',
    ),
    terminal_output=dict(nohash=True,
    ),
    transforms=dict(argstr='%s',
    mandatory=True,
    ),
    )
    inputs = ApplyTransformsToPoints.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_ApplyTransformsToPoints_outputs():
    output_map = dict(output_file=dict(),
    )
    outputs = ApplyTransformsToPoints.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value