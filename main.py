import numpy as np
import matplotlib.pyplot as plt


def build_graph(name_for_title, name_for_file, t, signal, frequencies, signal_spectrum):
    plt.figure(figsize=(12, 6))
    plt.suptitle(name_for_title + 'ая модуляция')

    plt.subplot(1, 2, 1)
    plt.plot(t, signal)
    plt.title(name_for_title + 'ая модуляция гармонического сигнала меандром')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')

    # signal_spectrum[0] = 0
    title_spectrum_graph = 'Спектр ' + name_for_title[0].lower() + name_for_title[1:] + ('ой модуляции гармонического '
                                                                                         'сигнала меандром')

    plt.subplot(1, 2, 2)
    plt.plot(frequencies[:len(frequencies) // 2], np.abs(signal_spectrum[:len(signal_spectrum) // 2]))
    plt.title(title_spectrum_graph)
    plt.xlabel('Частота, Гц')
    plt.xlim(0, 50)
    plt.ylabel('Амплитуда')

    plt.grid()
    plt.tight_layout()

    name_signal_graph = 'graphs/' + str(name_for_file) + '_modulation.png'
    plt.savefig(name_signal_graph)


def calculate_spectrum_and_build_graphs(signal, sampling_rate, t, name_for_title, name_for_file):
    signal_spectrum = np.fft.fft(signal)
    frequencies_for_signal_spectrum = np.fft.fftfreq(len(signal_spectrum), 1 / sampling_rate)

    build_graph(name_for_title, name_for_file, t, signal, frequencies_for_signal_spectrum, signal_spectrum)


def make_signals_and_their_modulations(frequency, sampling_rate, duration):
    t = np.linspace(0, duration, duration * sampling_rate)

    harmonic_signal = np.sin(2 * np.pi * frequency * t)
    digital_signal = np.where(harmonic_signal > 0, 1, 0)

    amplitude_modulated_signal = (1 + digital_signal) * harmonic_signal
    calculate_spectrum_and_build_graphs(amplitude_modulated_signal, sampling_rate, t, 'Амлитудн', 'amplitude')

    frequency_modulated_signal = np.sin(2 * np.pi * (frequency + digital_signal) * t)
    calculate_spectrum_and_build_graphs(frequency_modulated_signal, sampling_rate, t, 'Частотн', 'frequency')

    phase_modulated_signal = np.sin(2 * np.pi * frequency * t + 0.5 * digital_signal)
    calculate_spectrum_and_build_graphs(phase_modulated_signal, sampling_rate, t, 'Фазов', 'phase')


def main():
    frequency = 8
    sampling_rate = 1000
    duration = 1

    make_signals_and_their_modulations(frequency, sampling_rate, duration)


main()
