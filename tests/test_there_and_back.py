
"""
"There and back" tests for the Baudot library
"""

from io import StringIO, BytesIO

from hypothesis import given, strategies as st

from baudot import encode_str, decode_to_str, handlers
from baudot.codecs import ITA2_STANDARD, ITA2_US, ITA1_CONTINENTAL

# Note: ITA1_UK cannot be tested easily because it has two-character symbols
CODECS = (ITA1_CONTINENTAL, ITA2_STANDARD, ITA2_US)


@st.composite
def tape_config_strategy(draw):
    chars = st.characters(blacklist_categories=('Cc',))
    punch, blank, _sep = draw(st.sets(chars, min_size=3, max_size=3))
    sep = draw(st.one_of(st.just(''), st.just(_sep)))
    return handlers.TapeConfig(punch, blank, sep)


@st.composite
def codec_test_strategy(draw):
    codec = draw(st.sampled_from(CODECS))
    test_str = draw(st.text(alphabet=sorted(codec.alphabet)))
    return codec, test_str


@given(codec_test_strategy(), tape_config_strategy())
def test_tape_codec_tnb(codec_test, tape_config):
    codec, test_str = codec_test

    tmp_out = StringIO()
    writer = handlers.TapeWriter(tmp_out, tape_config)
    encode_str(test_str, codec, writer)

    tmp_out.seek(0)
    reader = handlers.TapeReader(tmp_out, tape_config)
    str_back = decode_to_str(reader, codec)

    tmp_out.close()
    assert str_back == test_str


@given(codec_test_strategy())
def test_hexbytes_codec_tnb(codec_test):
    codec, test_str = codec_test

    tmp_out = BytesIO()
    writer = handlers.HexBytesWriter(tmp_out)
    encode_str(test_str, codec, writer)

    tmp_out.seek(0)
    reader = handlers.HexBytesReader(tmp_out)
    str_back = decode_to_str(reader, codec)

    tmp_out.close()
    assert str_back == test_str
