###what is...
# pyFakeFifo
###and how does it work?

* First take data with Nevis Readout.
  * The repo is here: [NevisReadout](https://github.com/NevisUB/sn/tree/2stream).
  * Fake data collection with `mbtest_2stream_fake.c`.
  * Real data collection (activated ADCs) with fixed snova baseline with `mbtest_2stream_realFixedBaseline.c`.
  * Makefiles are in the `linux` directory.
* Next decode the data (first `hexdump` to make sure data is not corrupt.
  * Use the [NevisDecoder](https://github.com/vgenty/NevisDecoder) with the `larlite` [decoder beta branch](https://github.com/larlight/larlite/tree/nevis_decoder_beta)
  * In the `Decoder/mac` directory run `sn_tpc_huffman.py` or `tpc_huffman.py` for either snova or trigger stream (binary format is different...)
* Analysis
  * Can do some analysis with your own `larlite` module.
  * Try and display the data with this tool
  * Display with ``python view_fifo.py [dir | rootfiles]``
