class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bitString: int = 1
        for nucleotide in gene.upper():
            self.bitString <<= 2
            if nucleotide == "A": self.bitString |= 0b00
            elif nucleotide == "C": self.bitString |= 0b01
            elif nucleotide == "G": self.bitString |= 0b10
            elif nucleotide == "T": self.bitString |= 0b11
            else: raise ValueError("Invalid nucleotide: {}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bitString.bit_length() - 1, 2):
            bits: int = self.bitString >> i & 0b11
            if bits == 0b00: gene += "A"
            elif bits == 0b01: gene += "C"
            elif bits == 0b10: gene += "G"
            elif bits == 0b11: gene += "T"
            else: raise ValueError("Invalid bits: {}".format(bits))
        return gene[::-1]

    def __str__(self) -> str:
        return self.decompress()

if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print("original is {} bytes".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)  # compress
    print("compressed is {} bytes".format(getsizeof(compressed.bitString)))
    print(compressed)  # decompress
    print("original and decompressed are the same: {}".format(original ==
     compressed.decompress()))


