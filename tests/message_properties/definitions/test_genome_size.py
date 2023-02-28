from tol_lab_share.message_properties.definitions.genome_size import GenomeSize
from helpers import check_validates_string


def test_genome_size_is_string():
    check_validates_string(GenomeSize)
