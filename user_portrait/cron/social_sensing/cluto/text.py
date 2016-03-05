import os

CLUTO_FOLDER = 'cluto'
AB_PATH = "/home/ubuntu8/yuankun/new_version/user_portrait/user_portrait/social_sensing"
CLUTO_EXECUTE_PATH = './cluto-2.1.2/Linux-i686/vcluster'
cluto_input_folder = os.path.join(AB_PATH, CLUTO_FOLDER)

vcluster = os.path.join(AB_PATH, CLUTO_EXECUTE_PATH)
result_file = os.path.join(cluto_input_folder, '%s.clustering.%s' % ("24095.mat", 10))
evaluation_file = os.path.join(cluto_input_folder, '%s_%s.txt' % ("24095.mat", 10))

command = '%s -niter=20 %s %s > %s' % (vcluster, "24095.mat", 10, evaluation_file)
os.popen(command)


