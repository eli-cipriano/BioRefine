#test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run build_ethanol python biorefine.py --product Ethanol --file ethanol
assert_in_stdout "yeast -> ethanol"
assert_in_stdout "corn -> glucose"
assert_in_stdout "germ -> oil"
assert_exit_code 0
