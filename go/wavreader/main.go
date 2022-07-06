package main

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"os"
)

func ru16(src io.Reader) (uint16, error) {
	raw := []byte{0, 0}
	_, err := src.Read(raw)
	if err != nil {
		return 0, err
	}
	return binary.LittleEndian.Uint16(raw), nil
}

func ru32(src io.Reader) (uint32, error) {
	raw := []byte{0, 0, 0, 0}
	_, err := src.Read(raw)
	if err != nil {
		return 0, err
	}
	return binary.LittleEndian.Uint32(raw), nil
}

func wu16(num uint16, to io.Writer) error {
	raw := []byte{0, 0}
	binary.BigEndian.PutUint16(raw, num)
	_, err := to.Write(raw)
	return err
}

func wu32(num uint32, to io.Writer) error {
	raw := []byte{0, 0, 0, 0}
	binary.BigEndian.PutUint32(raw, num)
	_, err := to.Write(raw)
	return err
}

type SubChunk struct {
	ChunkID   []byte
	ChunkSize uint32
	Data      []byte
}

type RiffChunk struct {
	ChunkID   []byte
	ChunkSize uint32
	Format    []byte
}

type FmtChunk struct {
	ChunkID       []byte
	ChunkSize     uint32
	AudioFormat   uint16
	NumChannels   uint16
	SampleRate    uint32
	ByteRate      uint32
	BlockAlign    uint16
	BitsPerSample uint16
}

type Wave struct {
	Riff *RiffChunk
	Fmt  *FmtChunk
	Data *SubChunk
}

func getRiffChunk(r io.Reader) (*RiffChunk, error) {
	id := []byte{0, 0, 0, 0}
	r.Read(id)
	if idstr := string(id); idstr != "RIFF" {
		return nil, errors.New("unexpected chunk ID: " + idstr)
	}

	sizeRaw := []byte{0, 0, 0, 0}
	r.Read(sizeRaw)
	size := binary.LittleEndian.Uint32(sizeRaw)

	format := []byte{0, 0, 0, 0}
	r.Read(format)
	if fmtstr := string(format); fmtstr != "WAVE" {
		return nil, errors.New("unexpected RIFF format: " + fmtstr)
	}

	return &RiffChunk{ChunkID: id, ChunkSize: size, Format: format}, nil
}

func getSubChunk(r io.Reader) *SubChunk {
	id := []byte{0, 0, 0, 0}
	r.Read(id)

	sizeRaw := []byte{0, 0, 0, 0}
	r.Read(sizeRaw)
	size := binary.LittleEndian.Uint32(sizeRaw)

	data := []byte{}
	for x := 0; x < int(size); x++ {
		data = append(data, 0)
	}
	r.Read(data)

	return &SubChunk{ChunkID: id, ChunkSize: size, Data: data}
}

func readFmtChunk(raw *SubChunk) (*FmtChunk, error) {
	if idstr := string(raw.ChunkID); idstr != "fmt " {
		return nil, errors.New("unexpected chunk ID: " + idstr)
	}

	r := bytes.NewReader(raw.Data)

	audioFormat, err := ru16(r)
	if err != nil {
		return nil, err
	}
	numChannels, err := ru16(r)
	if err != nil {
		return nil, err
	}
	sampleRate, err := ru32(r)
	if err != nil {
		return nil, err
	}
	byteRate, err := ru32(r)
	if err != nil {
		return nil, err
	}
	blockAlign, err := ru16(r)
	if err != nil {
		return nil, err
	}
	bitsPsample, err := ru16(r)
	if err != nil {
		return nil, err
	}

	if err != nil {
		return nil, err
	}

	return &FmtChunk{
		ChunkID:       raw.ChunkID,
		ChunkSize:     raw.ChunkSize,
		AudioFormat:   audioFormat,
		NumChannels:   numChannels,
		SampleRate:    sampleRate,
		ByteRate:      byteRate,
		BlockAlign:    blockAlign,
		BitsPerSample: bitsPsample,
	}, nil
}

func getWave(src io.Reader) (*Wave, error) {
	riffChunk, err := getRiffChunk(src)
	if err != nil {
		return nil, err
	}

	fmtChunkRaw := getSubChunk(src)
	fmtChunk, err := readFmtChunk(fmtChunkRaw)
	if err != nil {
		return nil, err
	}

	dataChunk := getSubChunk(src)
	if dataid := string(dataChunk.ChunkID); dataid != "data" {
		return nil, errors.New("unexpected chunk ID: " + dataid)
	}

	return &Wave{Riff: riffChunk, Fmt: fmtChunk, Data: dataChunk}, nil
}

func getWavefile(fn string) (*Wave, error) {
	f, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	return getWave(f)
}

func (w *Wave) Dump(to io.Writer) error {
	var err error

	riff := w.Riff

	_, err = to.Write(riff.ChunkID)
	if err != nil {
		return err
	}
	err = wu32(riff.ChunkSize, to)
	if err != nil {
		return err
	}
	_, err = to.Write(riff.Format)
	if err != nil {
		return err
	}

	frmt := w.Fmt

	_, err = to.Write(frmt.ChunkID)
	if err != nil {
		return err
	}
	err = wu32(frmt.ChunkSize, to)
	if err != nil {
		return err
	}
	err = wu16(frmt.AudioFormat, to)
	if err != nil {
		return err
	}
	err = wu16(frmt.NumChannels, to)
	if err != nil {
		return err
	}
	err = wu32(frmt.SampleRate, to)
	if err != nil {
		return err
	}
	err = wu32(frmt.ByteRate, to)
	if err != nil {
		return err
	}
	err = wu16(frmt.BlockAlign, to)
	if err != nil {
		return err
	}
	err = wu16(frmt.BitsPerSample, to)
	if err != nil {
		return err
	}

	data := w.Data
	_, err = to.Write(data.ChunkID)
	if err != nil {
		return err
	}
	err = wu32(data.ChunkSize, to)
	if err != nil {
		return err
	}
	_, err = to.Write(data.Data)
	if err != nil {
		return err
	}

	return nil
}

func (w *Wave) DumpFile(fn string) error {
	f, err := os.Open(fn)
	if err != nil {
		return err
	}
	defer f.Close()
	return w.Dump(f)
}

func main() {
	fn := ""
	fmt.Print("Enter filename: ")
	fmt.Scanln(&fn)

	wave, err := getWavefile(fn)
	if err != nil {
		fmt.Println("could not load wavefile:", err)
		return
	}

	seconds := wave.Data.ChunkSize / wave.Fmt.ByteRate

	format := wave.Fmt
	fmt.Println("Channels:", format.NumChannels)
	fmt.Println("Sample Rate:", format.SampleRate)
	fmt.Println("Filesize:", wave.Riff.ChunkSize+8, "bytes")
	fmt.Println("Length in seconds:", seconds)
}
