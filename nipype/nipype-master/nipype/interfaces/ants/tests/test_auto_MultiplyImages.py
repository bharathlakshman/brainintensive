# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import MultiplyImages


def test_MultiplyImages_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    dimension=dict(argstr='%d',
    mandatory=True,
    position=0,
    usedefault=False,
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    first_input=dict(argstr='%s',
    mandatory=True,
    position=1,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    num_threads=dict(nohash=True,
    usedefault=True,
    ),
    output_product_image=dict(argstr='%s',
    mandatory=True,
    position=3,
    ),
    second_input=dict(argstr='%s',
    mandatory=True,
    position=2,
    ),
    terminal_output=dict(nohash=True,
    ),
    )
    inputs = MultiplyImages.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_MultiplyImages_outputs():
    output_map = dict(output_product_image=dict(),
    )
    outputs = MultiplyImages.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value