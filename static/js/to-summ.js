function to_summ(number) {
    let str = Math.floor(number) + ""; //make the integer a string
    let sub = str.substring(str.length - 3, str.length); //the last three characters
    newstr = " " + sub;
    let i = 1;
    while (sub.length >= 3) {
        sub = str.substring(str.length - ((i + 1) * 3), str.length - (i * 3)); //next three characters
        newstr = sub + " " + newstr; //append the characters
        i += 1;
    }
    return newstr;
}