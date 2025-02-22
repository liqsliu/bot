f1() {
  :
}

f2() {
  :
}

f3() {
  :
}

f4() {
  :
}

f5() {
  :
}

f=$1
$f

time for i in {1..1000000}; do
  f1
  f2
  f3
  f4
  f5
done




f() {
  :
}

case $1 in
1)
  f
  ;;
2)
  f
  ;;
3)
  f
  ;;
4)
  f
  ;;
5)
  f
  ;;
esac

time for i in {1..1000000}; do
  case 1 in
  1)
    f
    ;;
  2)
    f
    ;;
  3)
    f
    ;;
  4)
    f
    ;;
  5)
    f
    ;;
  esac

  case 2 in
  1)
    f
    ;;
  2)
    f
    ;;
  3)
    f
    ;;
  4)
    f
    ;;
  5)
    f
    ;;
  esac
  case 3 in
  1)
    f
    ;;
  2)
    f
    ;;
  3)
    f
    ;;
  4)
    f
    ;;
  5)
    f
    ;;
  esac
  case 4 in
  1)
    f
    ;;
  2)
    f
    ;;
  3)
    f
    ;;
  4)
    f
    ;;
  5)
    f
    ;;
  esac
  case 5 in
  1)
    f
    ;;
  2)
    f
    ;;
  3)
    f
    ;;
  4)
    f
    ;;
  5)
    f
    ;;
  esac

done
