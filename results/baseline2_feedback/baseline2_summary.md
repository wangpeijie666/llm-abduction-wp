# Baseline2 Feedback-Guided LLM Spec Generation

## Overall

| Status | Count |
| --- | ---: |
| Error | 2 |
| Fail | 13 |
| Invalid | 3 |
| Pass | 3 |

## By Dataset

| Dataset | Pass | Fail | Invalid | Error | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| svcomp | 3 | 13 | 3 | 2 | 21 |

## Per Case

| Dataset | File | Status | Best Round | Best Result | C File | WP Output |
| --- | --- | --- | ---: | --- | --- | --- |
| svcomp | 231.c | Pass | 1 | Pass_8_8 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/successful_files/svcomp/231.c |  |
| svcomp | 232.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/232/232.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/232/wp.txt |
| svcomp | 233.c | Pass | 1 | Pass_9_9 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/successful_files/svcomp/233.c |  |
| svcomp | 234.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/234/234.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/234/wp.txt |
| svcomp | 235.c | Fail | 3 | Fail_12_13 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/235/235.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/235/wp.txt |
| svcomp | 236.c | Pass | 2 | Pass_8_8 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/successful_files/svcomp/236.c |  |
| svcomp | 237.c | Fail | 1 | Fail_7_9 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/237/237.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/237/wp.txt |
| svcomp | 238.c | Fail | 1 | Fail_10_12 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/238/238.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/238/wp.txt |
| svcomp | 239.c | Fail | 1 | Fail_11_12 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/239/239.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/239/wp.txt |
| svcomp | 240.c | Fail | 4 | Fail_14_18 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/240/240.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/240/wp.txt |
| svcomp | 241.c | Fail | 4 | Fail_13_14 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/241/241.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/241/wp.txt |
| svcomp | 242.c | Fail | 2 | Fail_14_15 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/242/242.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/242/wp.txt |
| svcomp | 243.c | Fail | 3 | Fail_8_9 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/243/243.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/243/wp.txt |
| svcomp | 244.c | Fail | 1 | Fail_11_12 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/244/244.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/244/wp.txt |
| svcomp | 245.c | Error | 1 | Error | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/245/245.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/245/wp.txt |
| svcomp | 246.c | Fail | 2 | Fail_16_20 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/246/246.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/246/wp.txt |
| svcomp | 247.c | Fail | 5 | Fail_18_23 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/247/247.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/247/wp.txt |
| svcomp | 248.c | Fail | 1 | Fail_15_17 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/248/248.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/248/wp.txt |
| svcomp | 249.c | Error | 1 | Error | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/249/249.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/249/wp.txt |
| svcomp | 250.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/250/250.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/250/wp.txt |
| svcomp | 251.c | Fail | 1 | Fail_11_12 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/251/251.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline2_feedback/failed_cases/svcomp/251/wp.txt |
