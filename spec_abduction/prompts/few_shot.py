from __future__ import annotations


baseline1_fewshot_1_source_code ="""\
#include <stdio.h>

void incrstar (int *p)
{
    (*p)++;
}

void main()
{
    int x = 0;
    incrstar(&x);
    //@ assert x == 1;
}
"""


baseline1_fewshot_1_answer = """\
#include <stdio.h>

/*@ 
    requires \valid(p);
    assigns *p;
    ensures *p == \old(*p) + 1;
*/
void incrstar (int *p)
{
    (*p)++;
}

void main()
{
    int x = 0;
    incrstar(&x);
    //@ assert x == 1;
}
"""

baseline1_fewshot_2_source_code = """\
#include <stdlib.h>

int f(int n, int *p, int *q) {
    if (n > 0)
        *p = n;
    else
        *q = n;
    return n;
}

int main() {
    int a = 0;
    int b = 0;
    int ret = f(1, &a, &b);
    //@ assert a == 1;
    //@ assert ret == 1;
    ret = f(-1, &a, &b);
    //@ assert b == -1;
    //@ assert ret == -1;
    return 0;
}
"""

baseline1_fewshot_2_answer = """\
#include <stdlib.h>

/*@
    requires \valid(q);
    requires \valid(p);
    ensures \result == \old(n);
    behavior p_changed:
        assumes n > 0;
        ensures *p == n;
        assigns *p;
    behavior q_changed:
        assumes n <= 0;
        ensures *q == n;
        assigns *q;
    complete behaviors p_changed, q_changed;
    disjoint behaviors p_changed, q_changed;
*/
int f(int n, int *p, int *q) {
    if (n > 0)
        *p = n;
    else
        *q = n;
    return n;
}

/*@
    ensures \result == 0;
*/
int main() {
    int a = 0;
    int b = 0;
    int ret = f(1, &a, &b);
    //@ assert a == 1;
    //@ assert ret == 1;
    ret = f(-1, &a, &b);
    //@ assert b == -1;
    //@ assert ret == -1;
    return 0;
}
"""
baseline1_fewshot_3_source_code ="""\
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SIZE 10

int foo(uint32_t *map, uint32_t *key, uint32_t len)
{
    int ret = -1;

    for (int i = 0; i < len; i++)
	  {
		    if (map[i] == key[i])
		    {
			      ret = 0;
			      break;
		    }
	  }
	  return ret;
}

int main()
{
    uint32_t key1[SIZE] = {0, 0};
    uint32_t map1[SIZE] = {1, 1};

    int ret = foo(map1, key1, 1);
    //@ assert ret == -1;

    ret = foo(map1, key1, 2);
    //@ assert ret == -1;

    return 0;
}
"""
baseline1_fewshot_3_answer ="""\
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SIZE 10

/*@ 
    requires \valid_read(map+(0..len-1));
    requires \valid_read(key+(0..len-1));
    ensures \result == -1 || \result == 0;
    ensures \result == -1 ==> \forall integer i; 0 <= i < len ==> map[i] != key[i];
    ensures \result == 0 ==> \exists integer i; 0 <= i < len && map[i] == key[i];
    assigns \nothing;
*/
int foo(uint32_t *map, uint32_t *key, uint32_t len)
{
    int ret = -1;
    /*@
    loop invariant 0 <= i <= len;
    loop invariant ret == -1 || ret == 0;
    loop invariant ret == -1 ==> \forall integer j; 0 <= j < i ==> map[j] != key[j];
    loop invariant ret == 0 ==> (\exists integer j; 0 <= j < i && map[j] == key[j]);
    loop assigns i;
    */
    for (int i = 0; i < len; i++)
	  {
		    if (map[i] == key[i])
		    {
			      ret = 0;
			      break;
		    }
	  }
	  return ret;
}

int main()
{
    uint32_t key1[SIZE] = {0, 0};
    uint32_t map1[SIZE] = {1, 1};

    int ret = foo(map1, key1, 1);
    //@ assert ret == -1;

    ret = foo(map1, key1, 2);
    //@ assert ret == -1;

    return 0;
}
"""


baseline2_fewshot_1_source_code = """\
#include <stdio.h>

void incrstar (int *p)
{
    (*p)++;
}
void main()
{
    int x = 0;
    incrstar(&x);
    //@ assert x == 1;
}
"""

baseline2_fewshot_1_previous_code = """\
#include <stdio.h>

/*@
  requires \valid(p);
  assigns *p;
*/
void incrstar(int *p)
{
    (*p)++;
}

void main()
{
    int x = 0;
    incrstar(&x);
    //@ assert x == 1;
}
"""


baseline2_fewshot_1_verifier_feedback = {
    "status": "Fail",
    "wp_result_type": "Fail_4_5",
    "wp_stdout": r"""
  [kernel] Parsing results/baseline1_llm_direct/failed_cases/svcomp/232/test.c
  (with preprocessing)
  [wp] Warning: Missing RTE guards
  [wp] Warning: Goal Property:
  [wp] Warning: Goal Property:
  [wp] [Failure] typed_main_assert (Qed 2ms) (Alt-Ergo)
  [wp] Proved goals:    4 / 5
    Failed:          1

  Unproved goal details:
  Goal Assertion (file results/baseline1_llm_direct/failed_cases/svcomp/232/
  test.c, line 16):
  Assume { Type: is_sint32(x). }
  Prove: x = 1.
  Prover Alt-Ergo 2.2.0 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3servere6332fsock)

  Prover Z3 4.8.12 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3server385145sock)
    """,
    "wp_stderr": "",
}

baseline2_fewshot_1_answer = """\
#include <stdio.h>

/*@
  requires \valid(p);
  assigns *p;
  ensures *p == \old(*p) + 1;
*/
void incrstar(int *p)
{
    (*p)++;
}

void main()
{
    int x = 0;
    incrstar(&x);
    //@ assert x == 1;
}
"""

baseline2_fewshot_2_source_code = """\
#include <stdlib.h>

int f(int n, int *p, int *q) {
    if (n > 0)
        *p = n;
    else
        *q = n;
    return n;
}

int main() {
    int a = 0;
    int b = 0;
    int ret = f(1, &a, &b);
    //@ assert a == 1;
    //@ assert ret == 1;
    ret = f(-1, &a, &b);
    //@ assert b == -1;
    //@ assert ret == -1;
    return 0;
}
"""

baseline2_fewshot_2_previous_code = """\
#include <stdlib.h>

/*@
  requires \valid(p) && \valid(q);
  assigns *p, *q;
  ensures \result == n;
  ensures (n > 0) ==> (*p == n && *q == \old(*q));
  ensures (n <= 0) ==> (*q == n && *p == \old(*p));
*/
int f(int n, int *p, int *q) {
    if (n > 0)
        *p = n;
    else
        *q = n;
    return n;
}

int main() {
    int a = 0;
    int b = 0;
    int ret = f(1, &a, &b);
    //@ assert a == 1;
    //@ assert ret == 1;
    ret = f(-1, &a, &b);
    //@ assert b == -1;
    //@ assert ret == -1;
    return 0;
}
"""

baseline2_fewshot_2_verifier_feedback = {
    "status": "Fail",
    "wp_result_type": "Fail_11_13",
    "wp_stdout": r"""[kernel] Parsing results/baseline1_llm_direct/failed_cases/svcomp/232/test.c (with preprocessing)
[wp] Warning: Missing RTE guards
[wp] [Failure] typed_f_ensures_3 (Qed 17ms) (Alt-Ergo)
[wp] [Failure] typed_f_ensures_2 (Qed 17ms) (Alt-Ergo)
[wp] Proved goals:   11 / 13
  Failed:          2

Unproved goal details:
Goal Post-condition (file results/baseline1_llm_direct/failed_cases/svcomp/232/test.c, line 7) in 'f':
Let x = Mint_0[q].
Let x_1 = Mint_0[p <- f][q].
Assume {
  When: 0 < f.
  Have: valid_rw(Malloc_0, p, 1) /\ valid_rw(Malloc_0, q, 1).
}
Prove: x_1 = x.

---

Goal Post-condition (file results/baseline1_llm_direct/failed_cases/svcomp/232/test.c, line 8) in 'f':
Let x = Mint_0[p].
Let x_1 = Mint_0[q <- f][p].
Assume {
  When: f <= 0.
  Have: valid_rw(Malloc_0, p, 1) /\ valid_rw(Malloc_0, q, 1).
}
Prove: x_1 = x.
""",
    "wp_stderr": "",
}

baseline2_fewshot_2_answer = """\
#include <stdlib.h>

/*@
  requires \valid(p) && \valid(q);
  requires \separated(p, q);
  assigns *p, *q;
  ensures \result == n;
  ensures (n > 0) ==> (*p == n && *q == \old(*q));
  ensures (n <= 0) ==> (*q == n && *p == \old(*p));
*/
int f(int n, int *p, int *q) {
    if (n > 0)
        *p = n;
    else
        *q = n;
    return n;
}

/*@
  assigns \nothing;
*/
int main() {
    int a = 0;
    int b = 0;
    int ret = f(1, &a, &b);
    //@ assert a == 1;
    //@ assert ret == 1;
    ret = f(-1, &a, &b);
    //@ assert b == -1;
    //@ assert ret == -1;
    return 0;
}
"""


baseline2_fewshot_3_source_code = """\
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SIZE 10

int foo(uint32_t *map, uint32_t *key, uint32_t len)
{
    int ret = -1;

    for (int i = 0; i < len; i++)
	  {
		    if (map[i] == key[i])
		    {
			      ret = 0;
			      break;
		    }
	  }
	  return ret;
}

int main()
{
    uint32_t key1[SIZE] = {0, 0};
    uint32_t map1[SIZE] = {1, 1};

    int ret = foo(map1, key1, 1);
    //@ assert ret == -1;

    ret = foo(map1, key1, 2);
    //@ assert ret == -1;

    return 0;
}
"""

baseline2_fewshot_3_previous_code = """\
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SIZE 10

/*@
  requires 0 <= len;
  requires \valid_read(map + (0..len-1));
  requires \valid_read(key + (0..len-1));
  assigns \nothing;

  behavior exists_equal:
    assumes \exists integer i; 0 <= i < len && map[i] == key[i];
    ensures \result == 0;

  behavior no_equal:
    assumes \forall integer i; 0 <= i < len ==> map[i] != key[i];
    ensures \result == -1;

  complete behaviors;
  disjoint behaviors;
*/
int foo(uint32_t *map, uint32_t *key, uint32_t len)
{
    int ret = -1;

    for (int i = 0; i < len; i++)
    {
        if (map[i] == key[i])
        {
            ret = 0;
            break;
        }
    }
    return ret;
}

int main()
{
    uint32_t key1[SIZE] = {0, 0};
    uint32_t map1[SIZE] = {1, 1};

    int ret = foo(map1, key1, 1);
    //@ assert ret == -1;

    ret = foo(map1, key1, 2);
    //@ assert ret == -1;

    return 0;
}
"""

baseline2_fewshot_3_verifier_feedback = {
    "status": "Invalid",
    "wp_result_type": "Invalid",
    "wp_stdout": r"""
      WP summary and warnings:
  [kernel] Parsing results/baseline1_llm_direct/failed_cases/svcomp/232/test.c
  (with preprocessing)
  [wp] Warning: Missing RTE guards
  [wp] Warning: Goal Property (1/2):
  [wp] Warning: Goal Property (1/2):
  [wp] Warning: Goal Property:
  [wp] Warning: Goal Property:
  [wp] Warning: Goal Property:
  [wp] Warning: Goal Property:
  [wp] [Failure] typed_foo_assigns_part1 (Qed 7ms) (Alt-Ergo)
  [wp] Warning: Goal Property:
  [wp] Warning: Goal Property:
  [wp] [Failure] typed_foo_no_equal_ensures (Qed 49ms) (Alt-Ergo)
  [wp] [Failure] typed_foo_exists_equal_ensures (Qed 36ms) (Alt-Ergo)
  [wp] [Failure] typed_main_assert_2 (Qed 30ms) (Alt-Ergo)
  [wp] Proved goals:   12 / 16
    Failed:          4

  Unproved goal details:
  Goal Assigns nothing in 'foo' (1/2):
  Effect at line 28
  Assume {
    Type: is_uint32(len_0).
    (* Heap *)
    Type: (region(key_0.base) <= 0) /\ (region(map_0.base) <= 0) /\
        linked(Malloc_0).
    (* Pre-condition *)
    Have: 0 <= len_0.
    (* Pre-condition *)
    Have: valid_rd(Malloc_0, shift_uint32(map_0, 0), len_0).
    (* Pre-condition *)
    Have: valid_rd(Malloc_0, shift_uint32(key_0, 0), len_0).
  }
  Prove: false.
  Prover Alt-Ergo 2.2.0 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3server49ca74sock)

  Prover Z3 4.8.12 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3server0259aasock)

  ---

  Goal Post-condition for 'exists_equal' (file results/baseline1_llm_direct/
  failed_cases/svcomp/232/test.c, line 15) in 'foo':
  Assume {
    Type: is_uint32(len_0) /\ is_uint32(len_1) /\ is_sint32(foo_0) /\
        is_sint32(i).
    (* Heap *)
    Type: (region(key_0.base) <= 0) /\ (region(map_0.base) <= 0) /\
        linked(Malloc_0).
    (* Residual *)
    When: len_0 <= to_uint32(i).
    (* Pre-condition *)
    Have: 0 <= len_1.
    (* Pre-condition *)
    Have: valid_rd(Malloc_0, shift_uint32(map_0, 0), len_1).
    (* Pre-condition *)
    Have: valid_rd(Malloc_0, shift_uint32(key_0, 0), len_1).
    (* Pre-condition for 'exists_equal' *)
    Have: (Mint_0[shift_uint32(map_0, i_1)] = Mint_0[shift_uint32(key_0,
  i_1)]) /\
        (0 <= i_1) /\ (i_1 < len_1).
  }
  Prove: foo_0 = 0.
  Prover Alt-Ergo 2.2.0 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3server9923f4sock)

  Prover Z3 4.8.12 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3servercdb7a6sock)

  ---

  Goal Post-condition for 'no_equal' (file results/baseline1_llm_direct/
  failed_cases/svcomp/232/test.c, line 19) in 'foo':
  Assume {
    Type: is_uint32(len_0) /\ is_uint32(len_1) /\ is_sint32(foo_0) /\
        is_sint32(i) /\ is_uint32(Mint_0[shift_uint32(key_0, i)]) /\
        is_uint32(Mint_0[shift_uint32(map_0, i)]).
    (* Heap *)
    Type: (region(key_1.base) <= 0) /\ (region(map_1.base) <= 0) /\
        linked(Malloc_0).
    (* Pre-condition *)
    Have: 0 <= len_1.
    (* Pre-condition *)
    Have: valid_rd(Malloc_0, shift_uint32(map_1, 0), len_1).
    (* Pre-condition *)
    Have: valid_rd(Malloc_0, shift_uint32(key_1, 0), len_1).
    (* Pre-condition for 'no_equal' *)
    Have: forall i_1 : Z. ((0 <= i_1) -> ((i_1 < len_1) ->
        (Mint_1[shift_uint32(map_1, i_1)] != Mint_1[shift_uint32(key_1,
  i_1)]))).
    If to_uint32(i) < len_0
    Then {
      (* Then *)
      Have: Mint_0[shift_uint32(map_0, i)] = Mint_0[shift_uint32(key_0, i)].
      Have: foo_0 = 0.
    }
  }
  Prove: foo_0 = (-1).
  Prover Alt-Ergo 2.2.0 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3serverde7f2fsock)

  Prover Z3 4.8.12 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3serverd0c146sock)

  ---

  Goal Assertion (file results/baseline1_llm_direct/failed_cases/svcomp/232/
  test.c, line 48):
  Assume {
    Type: is_sint32(ret_0).
    (* Initializer *)
    Init: forall i : Z. ((0 <= i) -> ((i <= 1) -> (key1_0[i] = 0))).
    (* Initializer *)
    Init: forall i : Z. ((2 <= i) -> ((i <= 9) -> (key1_0[i] = 0))).
    (* Initializer *)
    Init: forall i : Z. ((0 <= i) -> ((i <= 1) -> (map1_0[i] = 1))).
    (* Initializer *)
    Init: forall i : Z. ((2 <= i) -> ((i <= 9) -> (map1_0[i] = 0))).
    (* Call 'foo' *)
    Have: (((forall i : Z. ((0 <= i) -> ((i <= 1) ->
             (map1_0[i] != key1_0[i])))) -> (ret_0 = (-1)))) /\
        (((exists i : Z. (map1_0[i] = key1_0[i]) /\ (0 <= i) /\ (i <= 1)) ->
         (ret_0 = 0))).
  }
  Prove: ret_0 = (-1).
  Prover Alt-Ergo 2.2.0 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3serverd129a4sock)

  Prover Z3 4.8.12 returns Failed
  [Why3 Error] Connection error: client_connect: connection failed: Operation
  not permitted (connect,) (socket_name=/tmp/why3server3b79c3sock)
    """,
    "wp_stderr": "",
}

baseline2_fewshot_3_answer = """\
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SIZE 10

/*@
  requires len <= 2147483647;
  requires \valid_read(map + (0..len-1));
  requires \valid_read(key + (0..len-1));
  assigns \nothing;

  behavior exists_equal:
    assumes \exists integer i; 0 <= i < len && map[i] == key[i];
    ensures \result == 0;

  behavior no_equal:
    assumes \forall integer i; 0 <= i < len ==> map[i] != key[i];
    ensures \result == -1;

  complete behaviors;
  disjoint behaviors;
*/
int foo(uint32_t *map, uint32_t *key, uint32_t len)
{
    int ret = -1;

    /*@
      loop invariant 0 <= len;
      loop invariant 0 <= i <= len;
      loop invariant ret == -1 || ret == 0;
      loop invariant ret == -1 ==> \forall integer j; 0 <= j < i ==> map[j] != key[j];
      loop invariant ret == 0 ==> \exists integer j; 0 <= j < i && map[j] == key[j];
      loop invariant (\forall integer j; 0 <= j < len ==> map[j] != key[j]) ==> ret == -1;
      loop assigns i, ret;
    */
    for (int i = 0; i < len; i++)
    {
        if (map[i] == key[i])
        {
            //@ assert 0 <= i < len;
            //@ assert map[i] == key[i];
            //@ assert !(\forall integer j; 0 <= j < len ==> map[j] != key[j]);
            ret = 0;
            break;
        }
    }
    return ret;
}

/*@
  assigns \nothing;
*/
int main()
{
    uint32_t key1[SIZE] = {0, 0};
    uint32_t map1[SIZE] = {1, 1};

    //@ assert map1[0] != key1[0];
    //@ assert \forall integer i; 0 <= i < 1 ==> map1[i] != key1[i];
    int ret = foo(map1, key1, 1);
    //@ assert ret == -1;

    //@ assert map1[0] != key1[0];
    //@ assert map1[1] != key1[1];
    //@ assert \forall integer i; 0 <= i < 2 ==> map1[i] != key1[i];
    ret = foo(map1, key1, 2);
    //@ assert ret == -1;

    return 0;
}
"""



BASELINE1_FEW_SHOTS = [
    {
        "source_code": baseline1_fewshot_1_source_code,
        "answer": baseline1_fewshot_1_answer,
    },
    {
        "source_code": baseline1_fewshot_2_source_code,
        "answer": baseline1_fewshot_2_answer,
    },
    {
        "source_code": baseline1_fewshot_3_source_code,
        "answer": baseline1_fewshot_3_answer,
    },
]


BASELINE2_FEW_SHOTS = [
    {
        "source_code": baseline2_fewshot_1_source_code,
        "previous_code": baseline2_fewshot_1_previous_code,
        "verifier_feedback": baseline2_fewshot_1_verifier_feedback,
        "answer": baseline2_fewshot_1_answer,
    },
    {
        "source_code": baseline2_fewshot_2_source_code,
        "previous_code": baseline2_fewshot_2_previous_code,
        "verifier_feedback": baseline2_fewshot_2_verifier_feedback,
        "answer": baseline2_fewshot_2_answer,
    },
    {
        "source_code": baseline2_fewshot_3_source_code,
        "previous_code": baseline2_fewshot_3_previous_code,
        "verifier_feedback": baseline2_fewshot_3_verifier_feedback,
        "answer": baseline2_fewshot_3_answer,
    },
]


# Backward-compatible aliases for older imports.
ACSL_GENERATION_FEW_SHOTS = BASELINE1_FEW_SHOTS
FEW_SHOT_EXAMPLES = BASELINE1_FEW_SHOTS
