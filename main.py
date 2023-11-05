import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert


def build_graph_for_signal(t, signal, title):
    plt.plot(t, signal)
    plt.title(title)
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')


def build_graph_for_spectrum(frequencies, signal_spectrum, title):
    plt.plot(frequencies[:len(frequencies) // 2], np.abs(signal_spectrum[:len(signal_spectrum) // 2]))
    plt.title(title)
    plt.xlabel('Частота, Гц')
    plt.xlim(0, 100)
    plt.ylabel('Амплитуда')


def build_graph_for_signal_and_his_modulations(name_for_title, name_for_file, t, signal, frequencies, signal_spectrum):
    plt.figure(figsize=(12, 6))
    plt.suptitle(name_for_title + 'ая модуляция')
    name_for_title += 'ая модуляция гармонического сигнала меандром'

    plt.subplot(1, 2, 1)
    build_graph_for_signal(t, signal, name_for_title)

    signal_spectrum[0] = 0

    plt.subplot(1, 2, 2)
    build_graph_for_spectrum(frequencies, signal_spectrum, 'Спектр')

    plt.grid()
    plt.tight_layout()

    name_signal_graph = 'graphs/' + str(name_for_file) + '_modulation.png'
    plt.savefig(name_signal_graph)


def get_spectrum(signal):
    return np.fft.fft(signal)


def get_frequencies_for_signal_spectrum(signal_spectrum, sampling_rate):
    return np.fft.fftfreq(len(signal_spectrum), 1 / sampling_rate)


def calculate_spectrum_and_build_graphs(signal, sampling_rate, t, name_for_title, name_for_file):
    signal_spectrum = get_spectrum(signal)
    frequencies_for_signal_spectrum = get_frequencies_for_signal_spectrum(signal_spectrum, sampling_rate)

    build_graph_for_signal_and_his_modulations(name_for_title, name_for_file, t, signal,
                                               frequencies_for_signal_spectrum, signal_spectrum)


def crop_spectrum_and_build__his_graph(signal_spectrum_abs, frequencies_for_signal_spectrum, cutoff):
    beginning_of_rise = local_maximum = 0
    is_upward_movement = True

    for i in range(1, 100):
        if is_upward_movement:
            if signal_spectrum_abs[i] >= signal_spectrum_abs[i - 1]:
                local_maximum = signal_spectrum_abs[i]
            else:
                is_upward_movement = False
        else:
            if signal_spectrum_abs[i] >= signal_spectrum_abs[i - 1]:
                if local_maximum < cutoff:
                    for index in range(beginning_of_rise, i - 1):
                        signal_spectrum_abs[index] = 0
                beginning_of_rise = i - 1
                is_upward_movement = True
                local_maximum = signal_spectrum_abs[i]

    plt.figure(figsize=(12, 6))
    build_graph_for_spectrum(frequencies_for_signal_spectrum, signal_spectrum_abs, 'Обрезанный спектр')

    plt.grid()
    plt.tight_layout()

    plt.savefig('graphs/cropped_signal_spectrum.png')


def crop_and_make_synthesize_and_filter_spectrum(amplitude_modulated_signal, sampling_rate, t):
    signal_spectrum = get_spectrum(amplitude_modulated_signal)
    frequencies_for_signal_spectrum = get_frequencies_for_signal_spectrum(signal_spectrum, sampling_rate)
    signal_spectrum[0] = 0

    signal_spectrum_abs = np.abs(signal_spectrum)

    crop_spectrum_and_build__his_graph(signal_spectrum_abs, frequencies_for_signal_spectrum, 100)

    synthesized_signal = np.fft.ifft(signal_spectrum_abs)

    envelope_function = hilbert(synthesized_signal.real)
    filtered_signal = np.where(np.abs(envelope_function) > 0.75, 1, 0)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    build_graph_for_signal(t, synthesized_signal.real, 'Синтезированный сигнал')

    plt.subplot(2, 1, 2)
    build_graph_for_signal(t, filtered_signal, 'Фильтрованный сигнал')

    plt.tight_layout()
    plt.savefig('graphs/synthesis_and_filter.png')


def get_harmonic_signal(frequency, t):
    return np.sin(2 * np.pi * frequency * t)


def make_signals_and_their_modulations(frequency, sampling_rate, duration):
    t = np.linspace(0, duration, duration * sampling_rate)

    harmonic_signal = get_harmonic_signal(frequency, t)

    frequency_for_digital_signal = 2
    digital_signal = np.where(get_harmonic_signal(frequency_for_digital_signal, t) > 0, 1, 0)

    amplitude_modulated_signal = digital_signal * harmonic_signal
    calculate_spectrum_and_build_graphs(amplitude_modulated_signal, sampling_rate, t, 'Амлитудн', 'amplitude')

    digital_signal = np.where(get_harmonic_signal(frequency_for_digital_signal, t) > 0, 2, 1)
    frequency_modulated_signal = get_harmonic_signal(frequency * digital_signal, t)
    calculate_spectrum_and_build_graphs(frequency_modulated_signal, sampling_rate, t, 'Частотн', 'frequency')

    digital_signal = np.where(get_harmonic_signal(frequency_for_digital_signal, t) > 0, 1, 0)
    phase_modulated_signal = np.sin(2 * np.pi * frequency * t + digital_signal)
    calculate_spectrum_and_build_graphs(phase_modulated_signal, sampling_rate, t, 'Фазов', 'phase')

    crop_and_make_synthesize_and_filter_spectrum(amplitude_modulated_signal, sampling_rate, t)


def main():
    frequency = 16
    sampling_rate = 1000
    duration = 1

    make_signals_and_their_modulations(frequency, sampling_rate, duration)


main()
