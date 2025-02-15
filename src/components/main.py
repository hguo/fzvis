from flask import Flask, request
from flask_cors import CORS
import json

import numpy as np

import libpressio
import math
# a way to upload the input data is needed
app = Flask(__name__)
# CORS(app, supports_credential=True)
CORS(app)
# ssh.close()
# print(stdout.read().decode())
@app.route('/indexlist',methods=["GET","POST"])
# 


def indexlist():
    def replace_unsupported_values(obj):
        if isinstance(obj, dict):
            return {k: replace_unsupported_values(v) for k, v in obj.items()}
        elif obj == math.inf:
            return "Infinity"  # 或者使用 None, 或者一个特定的值
        elif obj == -math.inf:
            return "-Infinity"  # 或者使用 None, 或者一个特定的值
        else:
            return obj
    def comparing_compressor(arguments):
        
        input_path = eval(arguments['input_data'])
        print(input_path)
        input_data = np.fromfile(input_path, dtype=np.float32)
        print(input_data)
        # print(eval(arguments["compressor_config"]))
        configs = {
                "compressor_id": arguments["compressor_id"],
                "early_config": arguments["early_config"],
                "compressor_config": arguments["compressor_config"],
                "bound":arguments["compressor_config"]["pressio:abs"]
            }
        
        def run_compressor(args):
            compressor = libpressio.PressioCompressor.from_config({
                # configure which compressor to use
                "compressor_id": args['compressor_id'],
                # configure the set of metrics to be gathered
                "early_config": args['early_config'],
                # {
                #     "pressio:metric": "composite",
                #     "composite:plugins": ["time", "size", "error_stat", "external"],
                #     "external:config_name": f"{args['compressor_id']}-{args['bound']:1.1e}",
                #     # "external:command": str(Path(__file__).absolute().parent.parent / "visualize.py")
                # },
                # configure the compressor
                "compressor_config": args['compressor_config']
                })
            decomp_data = input_data.copy()
            comp_data = compressor.encode(input_data)
            decomp_data = compressor.decode(comp_data, decomp_data)
            metrics = compressor.get_metrics()
            print('metrics',metrics)
            metrics1 = replace_unsupported_values(metrics)
            return {'compressor_id': configs["compressor_id"], 'bound': configs['bound'], 'metrics': metrics1}
        # result = {'compressor_id': 'sz', 'bound': 0.001, 'metrics': {'composite:compression_rate': 153609.83102918588, 'composite:compression_rate_many': None, 'composite:decompression_rate': 398406.374501992, 'composite:decompression_rate_many': None, 'error_stat:average_difference': 1.542031868511394e-06, 'error_stat:average_error': 5.690619636435443e-06, 'error_stat:difference_range': 0.0019998933421447873, 'error_stat:error_range': 0.000999949872493744, 'error_stat:max_error': 0.000999949872493744, 'error_stat:max_pw_rel_error': 105855014.7974729, 'error_stat:max_rel_error': 0.4882678768375195, 'error_stat:min_error': 0.0, 'error_stat:min_pw_rel_error': 5.612880037973005e-07, 'error_stat:min_rel_error': 0.0, 'error_stat:mse': 1.203790108682015e-09, 'error_stat:n': 25000000, 'error_stat:psnr': 35.420893822765464, 'error_stat:rmse': 3.469567853035901e-05, 'error_stat:value_max': 0.0020479534287005663, 'error_stat:value_mean': 8.596909993949838e-06, 'error_stat:value_min': 0.0, 'error_stat:value_range': 0.0020479534287005663, 'error_stat:value_std': 5.2587475532997e-05, 'external:error_code': 0, 'external:return_code': 0, 'external:runtime': 1.125545481, 'external:stderr': "Namespace(api=5, config_name='external', input=PosixPath('/home/yli/.pressioinbQTxLx'), decompressed=PosixPath('/home/yli/.pressioout0VXxIv'), dim=[500, 500, 100], type=<class 'numpy.float32'>)\n", 'size:bit_rate': 0.00940256, 'size:compressed_size': 29383, 'size:compression_ratio': 3403.3284552292143, 'size:decompressed_size': 100000000, 'size:uncompressed_size': 100000000, 'time:begin_check_options': None, 'time:begin_compress': 0, 'time:begin_compress_many': None, 'time:begin_decompress': 0, 'time:begin_decompress_many': None, 'time:begin_get_configuration': None, 'time:begin_get_options': 0, 'time:begin_set_options': 0, 'time:check_options': None, 'time:compress': 651, 'time:compress_many': None, 'time:decompress': 251, 'time:decompress_many': None, 'time:end_check_options': None, 'time:end_compress': 0, 'time:end_compress_many': None, 'time:end_decompress': 0, 'time:end_decompress_many': None, 'time:end_get_configuration': None, 'time:end_get_options': 0, 'time:end_set_options': 0, 'time:get_configuration': None, 'time:get_options': 0, 'time:set_options': 0}}
        # print(result['metrics'],)
        result = run_compressor(configs)
        print(result)
        # print(result)
        return result
    print('yes')
    if request.method == 'POST':
        # use the data from font-end json.load(request.data)
        
        compressor_id = json.loads(request.data)['compressor_id']
        print(eval(json.loads(request.data)['early_config']))
        early_config = json.loads(eval(json.loads(request.data)['early_config']))
        compressor_config = json.loads(eval(json.loads(request.data)['compressor_config']))
        input_data = json.loads(request.data)['input_data']
        
        # print(json.loads(early_config))
        # print('读入的shihou',type(json.loads(eval(compressor_config))))
        


        # with open(input_data, 'r') as file:
        #     data = json.load(file)
        
        configration = {'compressor_id':compressor_id, 
                        'early_config':early_config,
                        'compressor_config':compressor_config,
                        'input_data':input_data
                        }
        # comparing_compressor(configration)
        # print('输入的',early_config)
        # command = (
        #     f". /home/yli/lyx/spack/share/spack/setup-env.sh && "
        #     f"spack load libpressio && "
        #     f"python3 /home/yli/lyx/libpressio/test1/libpressio_tutorial/exercises/2_comparing_compressors/python/comparing_compressors.py {compressor_id} {early_config} {compressor_config} {input_data}"
        #     # f"python3 /home/yli/lyx/getdata.py {compressor_id} {early_config} {compressor_config} {input_data}"
        # )
        # e,stdout,stderr = ssh.exec_command(command)
        # output = stdout.read().decode('utf-8')
        # error = stderr.read().decode('utf-8')
        
        # # 处理输出
        # print("OUTPUT:")
        # print(output)
        # print(type(output))
        # # print(json.loads(output))
        # print("ERROR:")
        # print(error)
        # if error:return
        output = comparing_compressor(configration)
        # print('输出的事L:',json.dumps(json.loads(output)))
        return json.loads(json.dumps(output,indent=2))
    else:
        return 'configuration is illegal'



if __name__ == '__main__':
   app.run(host='164.107.120.231',debug=True)