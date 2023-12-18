import re
import sys
from time import sleep
import pandas as pd
from PrettyColorPrinter import add_printer

add_printer(1)
from usefuladb import AdbControl
from lxml2pandas import subprocess_parsing

adb = r"C:\Android\android-sdk\platform-tools\adb.exe"
AdbControl.connect_to_all_tcp_devices_windows(
    adb_path=adb,
)
addr = "127.0.0.1:5695"

eval_shell = AdbControl(
    adb_path=adb,
    device_serial=addr,
    use_busybox=False,
    connect_to_device=True,
    invisible=True,
    print_stdout=False,
    print_stderr=True,
    limit_stdout=3,
    limit_stderr=3,  # limits the history of shellcommands - can be checked at blocking_shell.stderr
    limit_stdin=None,
    convert_to_83=True,
    wait_to_complete=0,
    flush_stdout_before=True,
    flush_stdin_before=True,
    flush_stderr_before=True,
    exitcommand="xxxCOMMANDxxxDONExxx",
    capture_stdout_stderr_first=True,
    global_cmd=True,
    global_cmd_timeout=10,
    use_eval=True,  # executes commands using eval
    eval_timeout=60,  # timeout for eval (netcat transfer)
)
df = eval_shell.get_all_activity_elements(as_pandas=True)
x, y = df.loc[df.ELEMENT_ID == 'app:id/optional_toolbar_button'][['CENTER_X', 'CENTER_Y']].__array__()[0]
sleeptime = 1
script = """#!/bin/bash
cd /sdcard/Download
rm * -f
check_if_finished_writing() {
    timeout2=$(($SECONDS + timeoutfinal))
    while true; do
        if [ $SECONDS -gt "$timeout2" ]; then
            return 1
        fi
        initial_size=$(stat -c %s "$1")
        sleep "$2"
        current_size=$(stat -c %s "$1")
        if [ "$current_size" -eq "$initial_size" ]; then
            return 0
        fi
    done
}
while true; do
    input tap XCOORD YCOORD
    sleep SLEEPTIME
    file_contents=$(ls *.html -1 | tail -n 1)
    if [ -z "$file_contents" ]; then
        continue
    else
        if check_if_finished_writing "$file_contents" 0.1; then
            cat "$file_contents"
            rm * -f
        fi
    fi
    break
done""".replace('XCOORD', str(x)).replace('YCOORD', str(y)).replace('SLEEPTIME', str(sleeptime))
while True:
    try:
        stdout, stderr = eval_shell.execute_sh_command(script)
        htmldata = [(x[0].decode(), x[1]) for x in
                    re.findall(
                        br'<div><p>ELEMENTSEPSTART(\d+)</p></div>(.*?)<div><p>ELEMENTSEPEND\d+</p></div>'
                        , stdout[0])]
        df = subprocess_parsing(
            htmldata,
            chunks=1,
            processes=5,
            fake_header=True,
            print_stdout=False,
            print_stderr=True,
        )
        allelementsdf = df.loc[df.aa_attr_values == 'ovm-Fixture_Container']
        allframes = []
        for key, item in allelementsdf.iterrows():
            df2 = df.loc[df.aa_element_id.isin(item.aa_all_children) &
                         (df.aa_doc_id == item.aa_doc_id)]
            df3 = df2.loc[df2.aa_attr_values.isin(['ovm-ParticipantOddsOnly_Odds',
                                                   'ovm-FixtureDetailsTwoWay_TeamName'])]
            if len(df3) == 5:
                allframes.append(df3.aa_text.reset_index(drop=True).to_frame().T)
        dffinal = (pd.concat(allframes)).astype({2: 'Float64',
                                                 3: 'Float64', 4:
                                                     'Float64'}).reset_index(drop=True)
        print(dffinal)
    except Exception as e:
        sys.stderr.write(f'{e}\n')
        sys.stderr.flush()
