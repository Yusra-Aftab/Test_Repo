import whisper
import torch
import os
import time


def print_size_of_model(model):
    torch.save(model.state_dict(), "temp.p")
    size = os.path.getsize("temp.p")/1e6
    # print('Size (MB):', size)
    os.remove('temp.p')
    return size

def time_model_evaluation(model, mel, options,test_path, D_language ):
    eval_start_time = time.time()
    # result = whisper.decode(model, mel, options)
    result = whisper.transcribe(model, test_path,  language=D_language,)# , options)
    eval_end_time = time.time()
    eval_duration_time = eval_end_time - eval_start_time
    output = result["text"]
    print("Evaluate total time (seconds): {0:.1f}".format(eval_duration_time))
    return output


def process (audio_path):  
    

    model_fp32 = whisper.load_model(
        name="base",
        device="cpu")

    quantized_model = torch.quantization.quantize_dynamic(
        model_fp32, {torch.nn.Linear}, dtype=torch.qint8
    )

    print_size_of_model(model_fp32)
    print_size_of_model(quantized_model)

    # save/load using state dict
    path = 'qwhisper.pth'
    torch.save(quantized_model.state_dict(), path)

    test_path = audio_path
    audio = whisper.load_audio(test_path)
    audio = whisper.pad_or_trim(audio)

    mel   = whisper.log_mel_spectrogram(audio).to(model_fp32.device)
    options = whisper.DecodingOptions()

    # _, probs = model_fp32.detect_language(mel)
    # D_language = max(probs, key=probs.get)
    # print(D_language)

    # quantized
    _, probs = quantized_model.detect_language(mel)
    D_language = max(probs, key=probs.get)
    # print(D_language)


    # ## Evaluate the original FP32 WHISPER model
    # time_model_evaluation(model_fp32, mel, options)

    # Evaluate the INT8 WHISPER model after the dynamic quantization
    Full_text= time_model_evaluation(quantized_model, mel, options,test_path,D_language )
    print(Full_text)

    return Full_text




# process("speech.mp4")