# Baseline3 Assertion Probe

## Overall

| Status | Count |
| --- | ---: |
| Error | 1 |
| Fail | 34 |
| Invalid | 13 |
| Pass | 204 |

## By Dataset

| Dataset | Pass | Fail | Invalid | Error | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| 46_fib | 34 | 10 | 2 | 0 | 46 |
| SyGuS | 123 | 6 | 4 | 0 | 133 |
| frama-c-problem | 29 | 14 | 7 | 1 | 51 |
| svcomp | 17 | 4 | 0 | 0 | 21 |
| test | 1 | 0 | 0 | 0 | 1 |

## Per Case

| Dataset | File | Status | Best Attempt | Best Result | C File | WP Output | Trace |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| 46_fib | 134.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/134.c |  |  |
| 46_fib | 135.c | Fail | 1 | Fail_20_21 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/135/135.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/135/wp.txt |  |
| 46_fib | 136.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/136.c |  |  |
| 46_fib | 137.c | Fail | 1 | Fail_4_5 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/137/137.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/137/wp.txt |  |
| 46_fib | 138.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/138.c |  |  |
| 46_fib | 139.c | Fail | 3 | Fail_18_19 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/139/139.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/139/wp.txt |  |
| 46_fib | 140.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/140.c |  |  |
| 46_fib | 141.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/141.c |  |  |
| 46_fib | 142.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/142/142.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/142/wp.txt |  |
| 46_fib | 143.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/143.c |  |  |
| 46_fib | 144.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/144.c |  |  |
| 46_fib | 145.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/145.c |  |  |
| 46_fib | 146.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/146.c |  |  |
| 46_fib | 147.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/147.c |  |  |
| 46_fib | 148.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/148.c |  |  |
| 46_fib | 149.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/149.c |  |  |
| 46_fib | 150.c | Fail | 1 | Fail_14_15 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/150/150.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/150/wp.txt |  |
| 46_fib | 151.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/151.c |  |  |
| 46_fib | 152.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/152.c |  |  |
| 46_fib | 153.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/153.c |  |  |
| 46_fib | 154.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/154.c |  |  |
| 46_fib | 155.c | Fail | 2 | Fail_15_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/155/155.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/155/wp.txt |  |
| 46_fib | 156.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/156.c |  |  |
| 46_fib | 157.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/157.c |  |  |
| 46_fib | 158.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/158.c |  |  |
| 46_fib | 159.c | Fail | 2 | Fail_15_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/159/159.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/159/wp.txt |  |
| 46_fib | 160.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/160.c |  |  |
| 46_fib | 161.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/161.c |  |  |
| 46_fib | 162.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/162.c |  |  |
| 46_fib | 163.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/163.c |  |  |
| 46_fib | 164.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/164.c |  |  |
| 46_fib | 165.c | Fail | 2 | Fail_10_11 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/165/165.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/165/wp.txt |  |
| 46_fib | 166.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/166.c |  |  |
| 46_fib | 167.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/167.c |  |  |
| 46_fib | 168.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/168.c |  |  |
| 46_fib | 169.c | Fail | 1 | Fail_49_50 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/169/169.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/169/wp.txt |  |
| 46_fib | 170.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/170.c |  |  |
| 46_fib | 171.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/171.c |  |  |
| 46_fib | 172.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/172.c |  |  |
| 46_fib | 173.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/173.c |  |  |
| 46_fib | 174.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/174.c |  |  |
| 46_fib | 175.c | Fail | 3 | Fail_29_30 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/175/175.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/175/wp.txt |  |
| 46_fib | 176.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/176/176.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/176/wp.txt |  |
| 46_fib | 177.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/177.c |  |  |
| 46_fib | 178.c | Fail | 1 | Fail_41_42 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/178/178.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/46_fib/178/wp.txt |  |
| 46_fib | 179.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/46_fib/179.c |  |  |
| SyGuS | 1.c | Fail | 1 | Fail_12_13 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/1/1.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/1/wp.txt |  |
| SyGuS | 2.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/2.c |  |  |
| SyGuS | 3.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/3.c |  |  |
| SyGuS | 4.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/4.c |  |  |
| SyGuS | 5.c | Fail | 2 | Fail_8_9 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/5/5.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/5/wp.txt |  |
| SyGuS | 6.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/6.c |  |  |
| SyGuS | 7.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/7/7.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/7/wp.txt |  |
| SyGuS | 8.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/8.c |  |  |
| SyGuS | 9.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/9.c |  |  |
| SyGuS | 10.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/10.c |  |  |
| SyGuS | 11.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/11.c |  |  |
| SyGuS | 12.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/12/12.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/12/wp.txt |  |
| SyGuS | 13.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/13.c |  |  |
| SyGuS | 14.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/14.c |  |  |
| SyGuS | 15.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/15.c |  |  |
| SyGuS | 16.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/16.c |  |  |
| SyGuS | 17.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/17.c |  |  |
| SyGuS | 18.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/18.c |  |  |
| SyGuS | 19.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/19.c |  |  |
| SyGuS | 20.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/20.c |  |  |
| SyGuS | 21.c | Fail | 1 | Fail_11_12 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/21/21.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/21/wp.txt |  |
| SyGuS | 22.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/22.c |  |  |
| SyGuS | 23.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/23/23.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/23/wp.txt |  |
| SyGuS | 24.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/24/24.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/24/wp.txt |  |
| SyGuS | 25.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/25.c |  |  |
| SyGuS | 26.c | Fail | 2 | Fail_10_11 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/26/26.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/26/wp.txt |  |
| SyGuS | 27.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/27.c |  |  |
| SyGuS | 28.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/28.c |  |  |
| SyGuS | 29.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/29.c |  |  |
| SyGuS | 30.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/30.c |  |  |
| SyGuS | 31.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/31.c |  |  |
| SyGuS | 32.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/32.c |  |  |
| SyGuS | 33.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/33.c |  |  |
| SyGuS | 34.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/34.c |  |  |
| SyGuS | 35.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/35.c |  |  |
| SyGuS | 36.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/36.c |  |  |
| SyGuS | 37.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/37.c |  |  |
| SyGuS | 38.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/38.c |  |  |
| SyGuS | 39.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/39.c |  |  |
| SyGuS | 40.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/40.c |  |  |
| SyGuS | 41.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/41.c |  |  |
| SyGuS | 42.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/42.c |  |  |
| SyGuS | 43.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/43.c |  |  |
| SyGuS | 44.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/44.c |  |  |
| SyGuS | 45.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/45.c |  |  |
| SyGuS | 46.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/46.c |  |  |
| SyGuS | 47.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/47.c |  |  |
| SyGuS | 48.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/48.c |  |  |
| SyGuS | 49.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/49.c |  |  |
| SyGuS | 50.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/50.c |  |  |
| SyGuS | 51.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/51.c |  |  |
| SyGuS | 52.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/52.c |  |  |
| SyGuS | 53.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/53.c |  |  |
| SyGuS | 54.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/54.c |  |  |
| SyGuS | 55.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/55.c |  |  |
| SyGuS | 56.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/56.c |  |  |
| SyGuS | 57.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/57.c |  |  |
| SyGuS | 58.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/58.c |  |  |
| SyGuS | 59.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/59.c |  |  |
| SyGuS | 60.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/60.c |  |  |
| SyGuS | 61.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/61.c |  |  |
| SyGuS | 62.c | Fail | 3 | Fail_18_19 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/62/62.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/62/wp.txt |  |
| SyGuS | 63.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/63.c |  |  |
| SyGuS | 64.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/64.c |  |  |
| SyGuS | 65.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/65.c |  |  |
| SyGuS | 66.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/66.c |  |  |
| SyGuS | 67.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/67.c |  |  |
| SyGuS | 68.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/68.c |  |  |
| SyGuS | 69.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/69.c |  |  |
| SyGuS | 70.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/70.c |  |  |
| SyGuS | 71.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/71.c |  |  |
| SyGuS | 72.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/72.c |  |  |
| SyGuS | 73.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/73.c |  |  |
| SyGuS | 74.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/74.c |  |  |
| SyGuS | 75.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/75.c |  |  |
| SyGuS | 76.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/76.c |  |  |
| SyGuS | 77.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/77.c |  |  |
| SyGuS | 78.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/78.c |  |  |
| SyGuS | 79.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/79.c |  |  |
| SyGuS | 80.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/80.c |  |  |
| SyGuS | 81.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/81.c |  |  |
| SyGuS | 82.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/82.c |  |  |
| SyGuS | 83.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/83.c |  |  |
| SyGuS | 84.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/84.c |  |  |
| SyGuS | 85.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/85.c |  |  |
| SyGuS | 86.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/86.c |  |  |
| SyGuS | 87.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/87.c |  |  |
| SyGuS | 88.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/88.c |  |  |
| SyGuS | 89.c | Fail | 1 | Fail_10_11 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/89/89.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/SyGuS/89/wp.txt |  |
| SyGuS | 90.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/90.c |  |  |
| SyGuS | 91.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/91.c |  |  |
| SyGuS | 92.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/92.c |  |  |
| SyGuS | 93.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/93.c |  |  |
| SyGuS | 94.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/94.c |  |  |
| SyGuS | 95.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/95.c |  |  |
| SyGuS | 96.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/96.c |  |  |
| SyGuS | 97.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/97.c |  |  |
| SyGuS | 98.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/98.c |  |  |
| SyGuS | 99.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/99.c |  |  |
| SyGuS | 100.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/100.c |  |  |
| SyGuS | 101.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/101.c |  |  |
| SyGuS | 102.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/102.c |  |  |
| SyGuS | 103.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/103.c |  |  |
| SyGuS | 104.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/104.c |  |  |
| SyGuS | 105.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/105.c |  |  |
| SyGuS | 106.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/106.c |  |  |
| SyGuS | 107.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/107.c |  |  |
| SyGuS | 108.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/108.c |  |  |
| SyGuS | 109.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/109.c |  |  |
| SyGuS | 110.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/110.c |  |  |
| SyGuS | 111.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/111.c |  |  |
| SyGuS | 112.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/112.c |  |  |
| SyGuS | 113.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/113.c |  |  |
| SyGuS | 114.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/114.c |  |  |
| SyGuS | 115.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/115.c |  |  |
| SyGuS | 116.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/116.c |  |  |
| SyGuS | 117.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/117.c |  |  |
| SyGuS | 118.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/118.c |  |  |
| SyGuS | 119.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/119.c |  |  |
| SyGuS | 120.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/120.c |  |  |
| SyGuS | 121.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/121.c |  |  |
| SyGuS | 122.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/122.c |  |  |
| SyGuS | 123.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/123.c |  |  |
| SyGuS | 124.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/124.c |  |  |
| SyGuS | 125.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/125.c |  |  |
| SyGuS | 126.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/126.c |  |  |
| SyGuS | 127.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/127.c |  |  |
| SyGuS | 128.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/128.c |  |  |
| SyGuS | 129.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/129.c |  |  |
| SyGuS | 130.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/130.c |  |  |
| SyGuS | 131.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/131.c |  |  |
| SyGuS | 132.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/132.c |  |  |
| SyGuS | 133.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/SyGuS/133.c |  |  |
| frama-c-problem | 180.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/180.c |  |  |
| frama-c-problem | 181.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/181.c |  |  |
| frama-c-problem | 182.c | Fail | 1 | Fail_15_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/182/182.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/182/wp.txt |  |
| frama-c-problem | 183.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/183.c |  |  |
| frama-c-problem | 184.c | Fail | 2 | Fail_20_21 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/184/184.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/184/wp.txt |  |
| frama-c-problem | 185.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/185.c |  |  |
| frama-c-problem | 186.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/186.c |  |  |
| frama-c-problem | 187.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/187.c |  |  |
| frama-c-problem | 188.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/188.c |  |  |
| frama-c-problem | 189.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/189/189.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/189/wp.txt |  |
| frama-c-problem | 190.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/190.c |  |  |
| frama-c-problem | 191.c | Fail | 2 | Fail_19_20 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/191/191.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/191/wp.txt |  |
| frama-c-problem | 192.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/192.c |  |  |
| frama-c-problem | 193.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/193.c |  |  |
| frama-c-problem | 194.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/194/194.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/194/wp.txt |  |
| frama-c-problem | 195.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/195.c |  |  |
| frama-c-problem | 196.c | Fail | 2 | Fail_12_13 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/196/196.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/196/wp.txt |  |
| frama-c-problem | 197.c | Fail | 2 | Fail_11_12 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/197/197.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/197/wp.txt |  |
| frama-c-problem | 198.c | Fail | 3 | Fail_14_17 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/198/198.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/198/wp.txt |  |
| frama-c-problem | 199.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/199.c |  |  |
| frama-c-problem | 200.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/200/200.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/200/wp.txt |  |
| frama-c-problem | 201.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/201.c |  |  |
| frama-c-problem | 202.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/202.c |  |  |
| frama-c-problem | 203.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/203/203.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/203/wp.txt |  |
| frama-c-problem | 204.c | Fail | 2 | Fail_7_8 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/204/204.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/204/wp.txt |  |
| frama-c-problem | 205.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/205.c |  |  |
| frama-c-problem | 206.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/206.c |  |  |
| frama-c-problem | 207.c | Fail | 3 | Fail_14_15 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/207/207.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/207/wp.txt |  |
| frama-c-problem | 208.c | Fail | 3 | Fail_13_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/208/208.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/208/wp.txt |  |
| frama-c-problem | 209.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/209.c |  |  |
| frama-c-problem | 210.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/210.c |  |  |
| frama-c-problem | 211.c | Fail | 2 | Fail_14_15 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/211/211.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/211/wp.txt |  |
| frama-c-problem | 212.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/212.c |  |  |
| frama-c-problem | 213.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/213.c |  |  |
| frama-c-problem | 214.c | Fail | 1 | Fail_22_23 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/214/214.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/214/wp.txt |  |
| frama-c-problem | 215.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/215.c |  |  |
| frama-c-problem | 216.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/216/216.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/216/wp.txt |  |
| frama-c-problem | 217.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/217.c |  |  |
| frama-c-problem | 218.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/218/218.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/218/wp.txt |  |
| frama-c-problem | 219.c | Invalid | 1 | Invalid | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/219/219.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/219/wp.txt |  |
| frama-c-problem | 220.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/220.c |  |  |
| frama-c-problem | 221.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/221.c |  |  |
| frama-c-problem | 222.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/222.c |  |  |
| frama-c-problem | 224.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/224.c |  |  |
| frama-c-problem | 225.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/225.c |  |  |
| frama-c-problem | 226.c | Fail | 2 | Fail_10_11 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/226/226.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/226/wp.txt |  |
| frama-c-problem | 227.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/227.c |  |  |
| frama-c-problem | 228.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/frama-c-problem/228.c |  |  |
| frama-c-problem | 229.c | Fail | 1 | Fail_33_35 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/229/229.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/229/wp.txt |  |
| frama-c-problem | 230.c | Fail | 2 | Fail_13_14 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/230/230.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/230/wp.txt |  |
| frama-c-problem | 231.c | Error | 1 | Error | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/231/231.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/frama-c-problem/231/wp.txt |  |
| svcomp | 231.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/231.c |  |  |
| svcomp | 232.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/232.c |  |  |
| svcomp | 233.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/233.c |  |  |
| svcomp | 234.c | Fail | 1 | Fail_15_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/234/234.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/234/wp.txt |  |
| svcomp | 235.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/235.c |  |  |
| svcomp | 236.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/236.c |  |  |
| svcomp | 237.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/237.c |  |  |
| svcomp | 238.c | Fail | 1 | Fail_27_28 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/238/238.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/238/wp.txt |  |
| svcomp | 239.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/239.c |  |  |
| svcomp | 240.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/240.c |  |  |
| svcomp | 241.c | Fail | 1 | Fail_12_13 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/241/241.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/241/wp.txt |  |
| svcomp | 242.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/242.c |  |  |
| svcomp | 243.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/243.c |  |  |
| svcomp | 244.c | Fail | 3 | Fail_42_43 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/244/244.c | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/failed_cases/svcomp/244/wp.txt |  |
| svcomp | 245.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/245.c |  |  |
| svcomp | 246.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/246.c |  |  |
| svcomp | 247.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/247.c |  |  |
| svcomp | 248.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/248.c |  |  |
| svcomp | 249.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/249.c |  |  |
| svcomp | 250.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/250.c |  |  |
| svcomp | 251.c | Pass |  | Pass | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/svcomp/251.c |  |  |
| test | 235.c | Pass | 1 | Pass_16_16 | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/successful_files/test/235.c |  | /home/wangpeijie/wpj_2010215/spec_generation_abduction/results/baseline3_assertion_probe/traces/test/235 |
