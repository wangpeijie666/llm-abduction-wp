# Baseline1 Direct LLM Spec Generation

## Overall

| Status | Count |
| --- | ---: |
| Error | 1 |
| Fail | 16 |
| Invalid | 2 |
| Pass | 2 |

## By Dataset

| Dataset | Pass | Fail | Invalid | Error | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| svcomp | 2 | 16 | 2 | 1 | 21 |

## Per Case

| Dataset | File | Status | Best Attempt | Best Result | C File | WP Output |
| --- | --- | --- | ---: | --- | --- | --- |
| svcomp | 231.c | Pass | 1 | Pass_8_8 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/successful_files/svcomp/231.c |  |
| svcomp | 232.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/232/232.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/232/wp.txt |
| svcomp | 233.c | Pass | 3 | Pass_11_11 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/successful_files/svcomp/233.c |  |
| svcomp | 234.c | Fail | 2 | Fail_10_11 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/234/234.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/234/wp.txt |
| svcomp | 235.c | Fail | 1 | Fail_7_9 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/235/235.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/235/wp.txt |
| svcomp | 236.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/236/236.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/236/wp.txt |
| svcomp | 237.c | Fail | 2 | Fail_8_9 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/237/237.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/237/wp.txt |
| svcomp | 238.c | Fail | 1 | Fail_10_12 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/238/238.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/238/wp.txt |
| svcomp | 239.c | Fail | 2 | Fail_15_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/239/239.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/239/wp.txt |
| svcomp | 240.c | Fail | 1 | Fail_14_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/240/240.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/240/wp.txt |
| svcomp | 241.c | Fail | 2 | Fail_6_7 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/241/241.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/241/wp.txt |
| svcomp | 242.c | Fail | 3 | Fail_10_11 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/242/242.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/242/wp.txt |
| svcomp | 243.c | Fail | 3 | Fail_8_9 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/243/243.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/243/wp.txt |
| svcomp | 244.c | Fail | 4 | Fail_15_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/244/244.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/244/wp.txt |
| svcomp | 245.c | Error | 1 | Error | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/245/245.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/245/wp.txt |
| svcomp | 246.c | Fail | 3 | Fail_20_24 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/246/246.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/246/wp.txt |
| svcomp | 247.c | Fail | 3 | Fail_14_15 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/247/247.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/247/wp.txt |
| svcomp | 248.c | Fail | 5 | Fail_20_23 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/248/248.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/248/wp.txt |
| svcomp | 249.c | Fail | 2 | Fail_6_7 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/249/249.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/249/wp.txt |
| svcomp | 250.c | Fail | 3 | Fail_5_7 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/250/250.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/250/wp.txt |
| svcomp | 251.c | Fail | 1 | Fail_15_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/251/251.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline1_llm_direct/failed_cases/svcomp/251/wp.txt |
