# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:32:25 2019

@author: PRAMOD
"""
import email.parser 
import os, sys, stat,re,csv,datetime
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords

file_counter=0
header_writer=0


def extract_email_id(str_mail_id):
    emai_id=dataclean(str(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",str(str_mail_id))))
    if(emai_id==""):
        emai_id="None" 
    return emai_id

def remove_stopwords_subject(sentence):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [str.lower(w) for w in word_tokens if not w in stop_words]
    for char in ",[]'":
            filtered_sentence=str(filtered_sentence).replace(char,"")

    return filtered_sentence
    
def dataclean(strtoremove):
    strtemp=str(strtoremove)
    for char in ",[]'<>():":
            strtemp=strtemp.replace(char,"")
    strtemp=strtemp.replace("\n","")
    return strtemp

def compare_sub(sub):
    if len(sub.split())!=0:
        ham_prob=0
        for sub_word in sub.split():
            with open('sub_ham.csv','rt')as fh:
                for hrow in csv.reader(fh):
                    if sub_word==dataclean(hrow):
                        ham_prob+=1
            continue
         
        spam_prob=0
        for sub_word in sub.split():
            with open('sub_spam.csv','rt')as fh:
                for srow in csv.reader(fh):
                    if sub_word==dataclean(srow):
                        spam_prob+=1
            continue
       
        if (ham_prob+spam_prob)==0:
            prob=0
        else:
            prob=spam_prob/(ham_prob+spam_prob)

        return prob
    else:
        return 0

def compare_ipadd(ipadds):
    if len(ipadds.split())!=0:
        ham_prob=0
        for ip in ipadds.split():
            with open('ip_add_ham.csv','rt')as fh:
                for hrow in csv.reader(fh):
                    if ip==dataclean(hrow):
                        ham_prob+=1
            continue
         
        spam_prob=0
        for ip in ipadds.split():
            with open('ip_add_spam.csv','rt')as fh:
                for srow in csv.reader(fh):
                    if ip==dataclean(srow):
                        spam_prob+=1
            continue
       
        if (ham_prob+spam_prob)==0:
            prob=0
        else:
            prob=spam_prob/(ham_prob+spam_prob)

        return prob
    else:
        return 0



def compare_sender(sender_emails):
    if len(sender_emails.split())!=0:
        ham_prob=0
        for email_add in sender_emails.split():
            with open('sender_ham.csv','rt')as fh:
                for hrow in csv.reader(fh):
                    if email_add==dataclean(hrow):
                        ham_prob+=1
            continue
         
        spam_prob=0
        for email_add in sender_emails.split():
            with open('sender_spam.csv','rt')as fh:
                for srow in csv.reader(fh):
                    if email_add==dataclean(srow):
                        spam_prob+=1
            continue
       
        if (ham_prob+spam_prob)==0:
            prob=0
        else:
            prob=spam_prob/(ham_prob+spam_prob)

        return prob
    else:
        return 0
        
def ExtractHeaders(filename):
    if not os.path.exists(filename):
        print ("ERROR: input file does not exist:", filename)
        os.exit(1)
    fp = open(filename,errors='ignore')
    print(filename)
    
    global STP,STN,SFP,SFN,TOTAL_FILES,sub_accuracy
    global IPTP,IPTN,IPFP,IPFN,IP_accuracy
    global sender_TP,sender_TN,sender_FP,sender_FN,sender_accuracy
    global spam_TP,spam_TN,spam_FP,spam_FN,spam_accuracy
    
    
    TOTAL_FILES=TOTAL_FILES+1
    msg = email.message_from_file(fp)
    type_of_file=filename.find('spam',0,len(str(filename)))
    filetype= 0 if type_of_file==-1 else 1
    
    
    Subject=dataclean(msg.__getitem__("Subject"))
    filtered_subject=str(remove_stopwords_subject(Subject))
    
    Received_IP_Address=dataclean(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(msg.get_all("Received"))))
    
    sender_email_add=dataclean(extract_email_id(msg.__getitem__("From")))
  
    sub_prob=compare_sub(filtered_subject)
    sub_spam_prob= 1 if sub_prob>=0.5 else 0
    
    ip_add_prob=compare_ipadd(Received_IP_Address)
    ip_add_spam_prob=1 if ip_add_prob>=0.5 else 0
    
    sender_prob=compare_sender(sender_email_add)
    sender_spam_prob=1 if sender_prob>=0.5 else 0

    if filetype==1 and sub_spam_prob==1:
        STP=STP+1
    
    if filetype==1 and sub_spam_prob==0:
        SFN=SFN+1
        
    if filetype==0 and sub_spam_prob==1:
        SFP=SFP+1
        
    if filetype==0 and sub_spam_prob==0:
        STN=STN+1
    
    if filetype==1 and ip_add_spam_prob==1:
        IPTP=IPTP+1
    
    if filetype==1 and ip_add_spam_prob==0:
        IPFN=IPFN+1
        
    if filetype==0 and ip_add_spam_prob==1:
        IPFP=IPFP+1
        
    if filetype==0 and ip_add_spam_prob==0:
        IPTN=IPTN+1
        
    if filetype==1 and sender_spam_prob==1:
        sender_TP=sender_TP+1
    
    if filetype==1 and sender_spam_prob==0:
        sender_FN=sender_FN+1
        
    if filetype==0 and sender_spam_prob==1:
        sender_FP=sender_FP+1
        
    if filetype==0 and sender_spam_prob==0:
        sender_TN=sender_TN+1
    
    total_prob=sender_spam_prob+ip_add_spam_prob+sub_spam_prob
    spam_prob=1 if total_prob>=2 else 0    
     
    if filetype==1 and spam_prob==1:
        spam_TP=spam_TP+1
    
    if filetype==1 and spam_prob==0:
        spam_FN=spam_FN+1
        
    if filetype==0 and spam_prob==1:
        spam_FP=spam_FP+1
        
    if filetype==0 and spam_prob==0:
        spam_TN=spam_TN+1
    
    print("STP="+str(STP)+" SFN="+str(SFN)+" SFP="+str(SFP)+" STN="+str(STN)+" TOTAL_FILES="+str(TOTAL_FILES))
    print("sub_accuracy="+str(float(STP+STN)/float(STP+SFN+SFP+STN)*100))

    print("IPTP="+str(IPTP)+" IPFN="+str(IPFN)+" IPFP="+str(IPFP)+" IPTN="+str(IPTN)+" TOTAL_FILES="+str(TOTAL_FILES))
    print("IP_accuracy="+str(float(IPTP+IPTN)/float(IPTP+IPFN+IPFP+IPTN)*100))

    print("sender_TP="+str(sender_TP)+" sender_FN="+str(sender_FN)+" sender_FP="+str(sender_FP)+" sender_TN="+str(sender_TN)+" TOTAL_FILES="+str(TOTAL_FILES))
    print("sender_accuracy="+str(float(sender_TP+sender_TN)/float(sender_TP+sender_FN+sender_FP+sender_TN)*100))
    
    print("spam_TP="+str(spam_TP)+" spam_FN="+str(spam_FN)+" spam_FP="+str(spam_FP)+" spam_TN="+str(spam_TN)+" TOTAL_FILES="+str(TOTAL_FILES))
    
    if float(spam_TP+spam_FN+spam_FP+spam_TN)!=0:
        print("spam_accuracy="+str(float(spam_TP+spam_TN)/float(spam_TP+spam_FN+spam_FP+spam_TN)*100))
    

    
    email_df = pd.DataFrame({'filename':filename,
                             'Subject_prob':sub_prob,
                             'sub_spam_prob':sub_spam_prob,
                             'ip_add_prob':ip_add_prob,
                             'ip_add_spam_prob':ip_add_spam_prob,
                             'sender_prob':sender_prob,
                             'sender_spam_prob':sender_spam_prob,
                             'spam_prob':spam_prob,
                             'filetype': filetype},index=[0])
    if(file_counter==1):
        email_df.to_csv('sub_ipadd_NB_with_result.csv',mode='a',index=False)  
    else:
        email_df.to_csv('sub_ipadd_NB_with_result.csv',mode='a',header=False,index=False)
              
def ExtractHeaderFromFiles (srcdir):
    try:
        files = os.listdir(srcdir)
        global file_counter
        
        file_counter=0
     
        for file in files:
            file_counter+=1
            srcpath = os.path.join(srcdir, file)
            src_info = os.stat(srcpath)
            if stat.S_ISDIR(src_info.st_mode):
                ExtractHeaderFromFiles(srcpath)
            else:  
                ExtractHeaders (srcpath)
    except Exception as ve:
        print(srcpath)
        print(ve)
                        
###################################################################
#print ('Input source directory: ') #ask for source and dest dirs
#srcdir = input()
srcdir = "D:\Python\SPAMASSASSIN\Round_10"

#if os.path.exists("Extracted_data.csv") and os.path.exists("not_eng_words.txt"):
if os.path.exists("sub_ipadd_NB_with_result.csv"):
    os.remove("sub_ipadd_NB_with_result.csv")
    print("sub_ipadd_NB_with_result.csv is removed")
               
if not os.path.exists(srcdir):
    print ('The source directory %s does not exist, exit...' % (srcdir))
    sys.exit()
###################################################################
start_time=datetime.datetime.now()
STP=0
STN=0
SFP=0
SFN=0
IPTP=0
IPTN=0
IPFP=0
IPFN=0
sender_TP=0
sender_TN=0
sender_FP=0
sender_FN=0
spam_TP=0
spam_TN=0
spam_FP=0
spam_FN=0
spam_accuracy=0
TOTAL_FILES=0
sub_accuracy=0
IP_accuracy=0
sender_accuracy=0

ExtractHeaderFromFiles(srcdir)
end_time=datetime.datetime.now()

print("STP="+str(STP)+" SFN="+str(SFN)+" SFP="+str(SFP)+" STN="+str(STN)+" TOTAL_FILES="+str(STP+SFN+SFP+STN))
print("IPTP="+str(IPTP)+" IPFN="+str(IPFN)+" IPFP="+str(IPFP)+" IPTN="+str(IPTN)+" TOTAL_FILES="+str(IPTP+IPFN+IPFP+IPTN))
print("sender_TP="+str(sender_TP)+" sender_FN="+str(sender_FN)+" sender_FP="+str(sender_FP)+" sender_TN="+str(sender_TN)+" TOTAL_FILES="+str(sender_TP+sender_FN+sender_FP+sender_TN))
print("spam_TP="+str(spam_TP)+" spam_FN="+str(spam_FN)+" spam_FP="+str(spam_FP)+" spam_TN="+str(spam_TN)+" TOTAL_FILES="+str(spam_TP+spam_FN+spam_FP+spam_TN))

sub_accuracy=(float(STP+STN)/float(STP+SFN+SFP+STN))*100
IP_accuracy=(float(IPTP+IPTN)/float(IPTP+IPFN+IPFP+IPTN))*100
sender_accuracy=(float(sender_TP+sender_TN)/float(sender_TP+sender_FN+sender_FP+sender_TN))*100
spam_accuracy=(float(spam_TP+spam_TN)/float(spam_TP+spam_FN+spam_FP+spam_TN))*100

print("Sub_Accuracy="+str(sub_accuracy))
print("IPAccuracy="+str(IP_accuracy))
print("senderAccuracy="+str(sender_accuracy))
print("spam_Accuracy="+str(spam_accuracy))
print(end_time-start_time)


