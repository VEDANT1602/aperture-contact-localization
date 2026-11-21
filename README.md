# Timing a sixth rim contact when centering an elliptical aperture

Technical report by Vedant Thaker, Independent Researcher, Jeffersonville, Indiana. Correspondence: vedant.thaker1602@gmail.com.

How much time should a probe spend improving the estimated center of an aperture before moving there? For an ellipse with unknown shape, four axial contacts can leave the center ambiguous. A fifth, oblique contact identifies a generic noiseless conic, while the opposite endpoint supplies redundancy. Across 3,200 simulated offsets of one ellipse, that sixth endpoint lowered median center error from 0.294 to 0.139 mm. At a center tolerance of 0.25 mm and a deadline of 1.8 s, it gained 876 on-time accurate corrections when each contact cost 0.18 s, then lost 920 when each cost 0.22 s. The change follows from the travel left after probing. A fixture-specific timing inequality makes the comparison transferable to a device once probe duration and travel speed have been measured.

- [Read the paper](manuscript.pdf)
- [Read the plain-text manuscript](manuscript.md)
- [Reproduce the analysis and inspect the source and data records](study/README.md)
- [Software license](LICENSE) and [third-party terms](LICENSING.md)
- [Preparation record](study/PREPARATION.md)
- [Previous manuscript and supplements](https://github.com/VEDANT1602/aperture-contact-localization/tree/564b3879d618f6053d90dfd42009a98d37b4ad89)
