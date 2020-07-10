int str2int(char* src)
{
	int tmp = 0;
    int neg = 0;
    int i = 0;
    if(src[0] == '-')
    {
        neg = 1;
        i = 1;
    }
	char c;
    while(1)
	{
        c = src[i];
        if(c == 0)
            break;
		tmp *= 10;
		tmp += c - 48;
        ++i;
	}
    if(neg)     return (tmp - 2 * tmp);
	else        return tmp;
}

float str2flt(char* src)
{
    int tmp_i = 0;
    int tmp_i_d = 0;
    int tmp_d = 0;
    int tmp_d_d = 0;
    int tmp_p = 10;
    int dec = 0;
    int neg = 0;
    int pos = 0;
    if(src[0] == '-')
        neg = pos = 1;
    char chr;
    while(1)
    {
        chr = src[pos];
        if(chr == 0)
            break;
        if(!dec)
        {
            if(chr == '.')
                dec = 1;
            else
            {
                tmp_i *= 10;
                tmp_i_d = chr - 48;
                if(tmp_i_d < -1 || tmp_i_d > 10)
                    continue;
                tmp_i += tmp_i_d;
            }
        }
        else
        {
            tmp_d *= 10;
            tmp_d_d = chr - 48;
            if(tmp_d_d < -1 || tmp_d_d > 10)
                continue;
            tmp_d += tmp_d_d;
            tmp_p *= 10;
        }
        pos++;
    }
    tmp_p /= 10;
    float fin_i = tmp_i;
    float fin_d = (float)tmp_d / (float)tmp_p;
    return fin_i + fin_d;
}