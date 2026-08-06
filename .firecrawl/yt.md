![Thumbnail (1920x1080)](https://i.ytimg.com/vi/5aSuTGBk83A/maxresdefault.jpg)
# [Risk Visibility: From First Commit to Live Production](https://www.youtube.com/watch?v=5aSuTGBk83A)

**Visibility**: Public
**Uploaded by**: [AccuKnox](https://www.youtube.com/@accuknox)
**Uploaded at**: 2026-04-30
**Published at**: 2026-04-30
**Length**: 41:03
**Views**: 106
**Likes**: 9
**Category**: Entertainment

## Description

```
Speaker : Aditya Raj, Sr. Solutions Engineer @ AccuKnox 
Moderator : Chirath De Sliva, Pre Sales Engineer @ VSOne

Understanding the blind spots and limitations of public-cloud-only security tools
Exploring how a single control plane eliminates shadow estates and coverage gaps
Demonstrating unified policy enforcement across cloud, on-premises, and edge environments
Walking through practical use cases and real-world security challenges
Open Q&A with the speaker and moderator

See AccuKnox in Action: www.accuknox.com/demo
```

## Transcript

Yeah, so good morning everyone. Warm
welcome to our attendees joining from
India and Sri Lanka.
And I'm Shirat the silver pieces
engineer at VS1 and I'll be your
moderator for today's session.
And so we are VS1 one of the rapidly
growing value added distributor based in
Sri Lanka and the official distributor
for the Equinox.
So today we are joined by Aditya Raj
security engineer at Equinox. Aditya
welcome. Great to have you.
Thanks Shirat. Great to be here and good
morning everyone.
Really excited today to deep dive into
this topic where we'll discuss around
the different securities around your
different areas starting from the very
first coming to the run time how you
secure your entire workloads your DLC
and a lot more.
Yeah, so good to be here and thank you
so much Shirat for having me.
Thank you so much. So today's session is
called risk visibility from first commit
to live production. So over the next 30
minutes we'll cover the structural
problems most of the hybrid cloud
environments carry and Aditya will walk
us through you know how a single control
plane
um
changes that and we will run a live
demonstration of the Equinox platform
and take us through a real world use
cases.
And we will close with an open Q&A. You
can ask questions because of the house
rules I mean your mic is muted
throughout but the chat is open. Feel
free to
drop your questions as they come to your
mind and I'll bring them to Aditya at
the end.
Um so start the session. So Aditya let's
open with the scale of the problem. So
what does a typical hybrid hybrid cloud
environment look looks like for a
SME or an enterprise organization.
Uh and uh
why is that complexity is dangerous?
Aditya.
Yeah, so basically uh we know, right? Uh
like from mid to large companies, hybrid
is not just a words, right? It is
basically you have different steps,
different uh over different environment,
right? You're using clouds like AWS,
Azure, GCP, the major public cloud. Then
you have assets over on-premise like
pages, VM servers, right? And even if
you have IoT edge devices. So basically
it is scattered around different
environment, right? The big danger is
basically everything is disconnected.
You use different tools for different
area of security. Security teams are
trying to solve this puzzle of having
different tools, understanding the
security gaps there, right? But at the
end, you don't get a clear picture here,
right? You don't get to see everything
at one place or clear picture of your
entire security aspects. So that is what
we lack
here from mid to large companies. We
have this uh gap, right?
Yeah.
Uh understood. Yeah, uh so to my to my
understanding, so when the teams start
using AWS, Azure, or GCP environments
with on-prem and uh even uh edge setups
and legacy systems, so most probably,
Aditya, you will end up with operational
and visibility chaos, right? So
uh to eliminate this, most of your teams
you uh usually turn on their different
uh tools for the uh each environment.
Uh I mean, like uh over the time, those
environments become siloed.
And uh which means most of the time your
security team is uh flying blind uh
across the board.
So um having said that, uh I think the
audience would uh also agree with me.
Um most teams are already using cloud
native CSPM so
public cloud consoles
to address this
visibility operational chaos. So, why
aren't they enough for these kind of
hybrid environments?
Could you please elaborate on this
Aditya?
Sure, that's really good ask, right? So,
basically when we say like more security
tools, right? Every security teams have
certain tools they use for their
security, right? Some of them also goes
for the manual approach for the
security, right? But when we talk around
the cloud native tools or CSPMs, right?
The cloud security posture management.
So, cloud native tools is basically
built for that cloud, right? It works
really really great when it comes to
protecting their own specific cloud.
Like you have for AWS, you have for
Azure, you have for GCP, you have for
Oracle and many other cloud, right? They
work really perfectly inside their own
bubble, but the second the data the data
moves outside like from AWS to
on-premise server, you lose the sight of
it. You just aren't basically the tool
itself isn't made for the world where
everything is a scattered from cloud to
on-premise to bare metals to IoT
devices, right? And that is why there
are different tools, but again all those
different tools give different insight
and you cannot see everything at one
place and that is where we lack the
insight of our security.
Got it, got it, got it. So,
the default console gives you like a
view, right? So, but the never the full
picture.
So, actually Aditya, I've seen this
happening. I mean everything looks
perfect fine on the AWS or Azure
dashboard, all green, no alerts. I mean
the team is chilling.
But the till someone spun up a temporary
cloud, connected back to their on-prem
system. So, I mean like that's the
tricky part, right? So, it's not an
like obvious failure. So, there's no red
alarms, no catastrophic signals
screaming for your attention. But it
just sits there under the shadows
waiting to be exploded.
Aditya.
Uh
and to be honest
I think it's waiting to be discovered at
the worst possible time, Aditya. So, um
we keep talking about blind spots and
hidden gaps. So, what are what what
actually lives in these blind spots and
what security teams are unknowingly
missing? Aditya.
Yeah, so basically there are variety of
things that can be a part of those blind
spots. If I give you some examples,
right? Like when we look in those blind
spots, right?
Uh usually we find some unpatched
servers, right? That cloud scanners
cannot detect because that is not in
their native cloud environment. It's
over on-premise. It's somewhere else in
private cloud, right? Somewhere where
the cloud scanners cannot reach, right?
That is where we see some unpatched
servers, we find some unprotected
controllers, containers where there
isn't any security rules enforced,
right? We also like find some shadow
resources which has not been detected
till now, right? And yeah, we just
forget about those things, right? And
then we detected it's like, "Oh, we got
this. This was actually there."
Yeah, something like this happens.
Absolutely. Absolutely. Absolutely agree
agree with you, Aditya. So, I mean like
after the deployment, it often like feel
like the job is done, right? So, and I
believe that's exactly where the
visibility starts starts to fade. I
mean, you know, just a little by little.
I mean, the assets are slipping over
your control, your radar, and you will
sense it, right? It It will show up
through anomalies like in your FinOps
dashboards, and similar signal across
environment. So, my question is, Aditya,
when do security teams first sense or
discover these gaps?
So, what's their typical reaction? Are
they surprised, or do most already sense
something is missing?
Yeah, so most security teams, like they
always have a gut feeling that something
is missing. You know, security teams,
they always play around security, and
they do have this gut feeling, something
is missing, but they can't prove it. The
problem is the tool which they're
currently using, it always gives them a
clean dashboard, like everything is good
here, you have the security in place,
but yeah, something is missing there,
right? And that is what we were looking
around those blind spots, or the dark
spots, where we were never able to reach
actually, right? And when we reach
there, when we saw those things, the
reality is often very disappointing than
those green dashboard, always looking
into the those green dashboard and
seeing like everything is secure.
Yeah, true. So,
let me ask the next obvious question is,
so how do we fix it? More importantly,
how do we solve this in a
practical way? So,
Aditya, so this is where I want to bring
AccuKnox in, right? So, please walk us
through how AccuKnox approach this, and
what makes a single control plane across
hybrid environments not only actually
possible, but at a scale.
Yeah, so basically, AccuKnox itself
CNAPP vendor, a cloud-native application
protection platform, that is something
that we have to offer. And when we say
CNAPP, right? And when we say other dark
sports, CNAPP, we relate these two
terms, right? Our approach in terms of
security is to provide a complete zero
trust security
to the user, to the companies, end
users, right? And uh yeah, we were
talking around the hybrid infrastructure
from cloud to on premise, right? So, at
AccuKnox, we secure your entire CSDLC
structure from the coding phase till the
runtime right? The secret sauce at
runtime is eBPF, extended Berkeley
Packet Filtering Framework. This is
something providing you uh like kernel
level visibility, your app behavior
visibility at real time, right? So, you
have different APIs, you have uh like
happy software, right? It all gets
monitored using eBPF, no matter your
environment. It can be cloud, it can be
on premise, right? Wherever you have
hosted your servers, right? So, in a
way, we provide you consistent
visibility over your app behavior,
right? Nothing gets outside of the site,
right? Everything is being monitored
having a deep kernel level visibility
over your app behavior, no matter where
it is deployed, right? And uh once you
see it, you can always protect it,
right? So, that is where uh we tend to
secure your entire workloads at runtime
as well as the entire SDLC. We'll talk
around it later on this uh session, like
how we provide a complete set of
security.
Right.
Absolutely, absolutely. So, um
this uh leads to my next question, uh
Aditya. So, uh beyond visibility, uh how
does AccuKnox uh move from just seeing
problems, observing problems to actually
preventing them? Like can we stop the
lateral movements, or can it be uh
proactive? Uh and um I think this would
be the most important question here. How
do we receive reduce the attack window
to near zero, which means real-time
prevention? I know it's a lot of
questions, Aditya.
You can answer. Yeah, it's uh it's
really fine. And this one is really
really good, right? You all know, right?
Having visibility is one thing, but
protection is another thing which we are
most concerned about, right? You just
seeing everything doesn't solve the
problem, right? Just seeing everything
is not enough. Right? Most tools most
tools uh which are already present in
the market, what they do is they detect
issues. They send you alerts, and then
you have to respond to those alerts,
right? By the time you respond to those
alerts, the damage is already done.
Now, at Illumio, what do we do? We
actually uh stop those attacks as they
happen. So, our approach is using eBPF,
monitoring your app behavior, providing
you visibility over your app behavior,
and then white-listing it. The term
white-listing is something very
uh very well-known in security, right?
The term white-listing and
black-listing. White-listing is
something where you choose what you want
to allow, right? And when we have this
level of control, this level of granular
control in an application, we choose
what to allow there, right? And
everything else gets blocked. So, uh
like in a nutshell, it's a kind of
white-listing approach where we choose
what your app requires, we allow it, we
block everything else by default. So,
it's not like detect and respond, we
know
what is uh required there, right? So,
it's kind of detecting, stopping the
attack, providing you alerts as well.
We won't allow any kind of attack there.
Right? And that's a kind of complete
zero trust security. By the way, this
one was uh really good questions, and uh
this is really a key differentiator as
well, right?
Okay. So, uh yeah. So, hearing that,
uh Aditya, so I've got to ask this. So,
I think a lot of people in this audience
are probably thinking the same. So, I
mean, like chances are most teams are
likely have invested in the security
tooling, right? So, across their code
bases, across their pipelines, or their
runtime environments. So,
I mean, like a very few are
starting from scratch, right, Aditya?
So, what we'd like to know
for the teams already invested in this
existing tooling, how does Aquinox fit
in?
Is it a rip and replace conversation or
something different?
Great. So, basically, Aquinox is not
made to, like,
provide you a different tool on set of
all the tools you're already having,
right? We mean to simplify things,
right? Aquinox always meant to simplify
things. We plug right into your existing
pipelines, your security workflows.
Whatever tools you're already utilizing
at your place, right? We can integrate
with those security toolings as well to
provide you
a single pane of visibility, right? One
dashboard where you have your entire
coverage, right? The goal for us is to
replace the clunky tools, right? Not
just give you another screen to look at,
right?
For rollout, we start out silently just
to watch and map things out, right?
Basically, analyzing your app behavior,
which I was just explaining in the
previous answer, right? Once you know
what's normal in your app behavior,
right? In your application security
pipeline, your application security
posture, and your infrastructure
security posture, right? You define a
baseline there.
You know that this is normal, you define
this baseline there, right? Anything
which goes outside of your defined
>> Is that?
Hello.
So, we are waiting for Aditya to be
joined. I think he's
kind of having an internet
I mean internet issue.
Let's give him a couple of seconds to
rejoin.
Aditya, you there?
I'm trying to
No, it is you are audible.
I think this is about where we
showcase the platform actually. So,
>> Hello. Can you hear me? Hey Jared.
Uh hi Aditya. Yeah.
I can hear you.
Great. Great. Apologies. I
think that this erupted.
No worries.
Uh
So, shall we continue
as we planned?
Uh
Yeah, we can.
Okay, so
when referring
to your
um
last
explanation, so
it's about like
the consolidation or addition, right?
So, we are not ripping off the existing
tools and replacing with another tool
that might need thousand other
thousand other modules to uh
fully uh uh uh
scan your environment.
So, Aditya, I won't take much time
because we have lost uh lost I mean two
or three minutes.
So, we can bring this to life, right?
So, please take us to the AccuKnox
platform, Aditya, and
show us you know
what a full hybrid visibility is
actually look like.
Is it possible to share your screen,
Aditya?
I think we lost him again.
Okay, we lost him.
We'll give him a
Yeah, we'll give him a couple of
minutes, yeah.
Hello, Aditya. Welcome back.
Hey, uh can you hear me now? Yes,
crystal clear. Yes, great. Let's
continue. So, we had to like discuss
around like how AccuKnox can provide
security, right? In a practical manner.
So, what I'll do is I'll quickly share
my screen, right? And then we'll cover
the security aspects of different areas
like in an hybrid environment, right?
So, just a second. I'll quickly share my
screen.
Yeah, please let me know when it is
visible to you guys.
Sure, sure. Yeah.
Uh so, we can see your browser. Okay, we
can see it now.
Uh you see my screen now? Yes.
Cool.
Yeah, so first of all apologies. I had
this internet disruption feeling really
first today.
I don't know why this happened today
itself, but yeah, uh
Okay, uh we were talking around hybrid
security, right? Like having
different tools for your security,
right? And it is really hard to manage
those security tools and it is really
hard to like understand your current
security gaps, right? And fulfill those
gaps. So, that is where Equinox comes
into picture, right? We have this CNAP
we were talking around is like how we
like kind of
connect different dots from cloud scale
to your on-premise environment like your
VMs, your bare metals, your IoT edge
devices, right? Now, uh like on this
platform itself, you find different
sorts of modules, different use cases,
right? And all of them won't be relevant
in these cases, but yeah, there are
certain things which is relevant from
CI/CD like perspective, right?
When I say CI/CD perspective, your
continuous integration, continuous
deployment pipelines sort of
perspective, right? Your SDLC, the
software development life cycle.
Uh when you write code, right? Uh that
is where we uh scan the code, we try to
understand the code related security
issues in that particular time, right?
And then we first uh mitigate, we first
uh like secure those codes just to make
sure that whatever code uh we are
pushing to our application does not
contain any uh like security
vulnerabilities there,
right? So, that is one thing.
Now,
I am not sure what is happening.
Uh can you hear me?
We can hear you, Aditya, and also can
see your screen as well.
So, we are uh the uh finding summary
page.
Okay, cool. So, I was explaining about
this thing, right? Uh you see my screen,
right?
We can see it. Yeah, I'm kind of stuck,
but uh
cool. Yeah. So, as you see, right? Uh
there is cloud finding, cluster finding,
IACs, AI, uh code, image, and
application, right? All these findings
are from different environment. All
these findings are different use cases
itself, right? Now, when we say your
IACs, your clusters, or code, right? It
is not necessarily dependent upon a
cloud, like major public cloud, AWS,
Azure, GCP. It can be from your CI/CD,
it can be from your on-premise hosted,
self-hosted CI/CD pipeline, your
self-hosted applications, right? Where
we do scans for code, images, right? And
that is where we provide complete
coverage in terms of uh
SDLC security. No matter where it is
hosted, no matter what kind of
environment are there,
Right?
So, I'll just quickly
dive into the details, but I think I'm
kind of stuck here.
Just
give me a minute.
No worries, take your time.
Uh sorry, guys. So, I was disconnected
from the internet and
I had to join again and
So, where is Aditya?
>> [laughter]
>> So, he's not here.
Uh
let me check on him. Okay.
>> Uh Aditya.
Hey, uh you see my screen?
Uh not yet Aditya.
Now we can see.
Okay, am I audible?
You are. You are.
Cool. I won't take much. I think my
system is really malfunctioning today.
So, I'll just quickly cover the things
here.
Apologies, guys. No worries Aditya. It
happens. Yeah, no worries.
You can go ahead. Yeah.
Right. [snorts] So, I was explaining
like how we connect dots from cloud to
your on-premise. Right? The dots where
most of the security teams were not able
to see right? Uh
the things or the findings which were
like never detected. Right? Uh dark
spots which we call.
Now, once we connect these dots like if
I talk around a specific use case, your
containers. Right? You can have
containers hosted over your cloud. You
can have containers running in your
Kubernetes clusters. It can be a managed
unmanaged like over your cloud or over
on-premise. It can be over private
cloud. Right? And it can be also over
registries, registries like ECR, ACR,
GAR, and then self-hosted registries as
well, right? Now, if you use different
tools, right? Or even if you use a
single tool, it scan different
environment, right? For one particular
use case,
then you kind of lost visibility in
terms of analyzing the particular
security aspects of your container
throughout different environment. Right?
So, that is just one use case. Now, if
we see the broader scope, broader scope
as in the entire CLC, the software
development life cycle. You have codes,
developer writes code, right? For your
application, you scan the code, you use
a different tool for code scanning. Then
you create a container, you use a tool
for container image scanning, right?
Then for your application dynamic
testing, the VAPT part, right? There you
either rely on manual pen tester, right?
An organization which does VAPT for you,
or you rely on a tool that will do VAPT
for you.
And then there are several other use
cases for STLC, the application
security, like VM security, and then
comes the malware security, like malware
security from malwares. So, all these
things, different security tools, and
all those security tools giving you a
clean sense of dashboard, right? A false
sense of security, where you most of the
time you miss on the real security
issues that is really impacting your
application at runtime.
Right? Now, if I give you an example, so
you see this container image finding at
Acunex, right? This is our platform. We
have this container image finding, and
the count is really very high, 39,346.
You use any different tools in the
market for like this thing,
uh container image scan, you will get a
lot of container image findings, right?
Now, the thing here is how to prioritize
these findings, right?
It is coming from different environment,
but how to prioritize which finding is
really impacting our environment, the
one which we are very much concerned
about. To do that, what we'll do is we
just quickly
prioritize these findings based on the
like severity.
Right? Like let's say we have 39,340
six findings, right? And I just want to
see the critical ones.
What I'll do is I'll just quickly cover
the critical ones. And not only
critical, we have a way to identify if
your findings is
like actually impacting at run time.
Right? So, run time verified, I'll just
make it yes.
This is a cool feature, by the way. So,
in case you are getting findings from
different tools, a lot of findings are
there, right? You want to understand how
to prioritize those findings and which
finding is like really impacting your
assets at run time, then you have this
flag over here, you just make it yes,
and then you get to see only a few
findings which you need to be concerned
about.
Right?
Awesome. Awesome. Awesome. I think
Aditya was able to
really bring the platform story together
in a very practical way. So, Aditya just
showed like
how we how you actually move from
fragmented visibility to deep full
contextual understanding, right? So,
and then that's really helped to
set the next segment which is use cases,
Aditya. So, before we get into the use
cases, anything that you want to flag
that we didn't get to show, Aditya?
Yeah, there is uh
Please let me know Sherrod when my
screen when I stop sharing the screen.
I think I can see myself in your screen.
Okay. So,
yeah. So, I was not able to share the
complete picture of Equinox, right, due
to
my very very bad network today. Yes,
unfortunately, yeah.
We will have another another webinar,
another discussion for another day.
Yeah, no worries. I'll arrange it. I
personally arrange it, okay?
Sure, we'll have it. So, you were saying
like before we move to the different
next segment, if there is anything to
point out here. Right, there is surely a
lot of things, but I'll just point out
one. Right, when we say runtime security
like having a single visibility and
monitoring over your application from
different environment, right, on a
hybrid environment, right, it's not just
monitoring, it is enforcing as well,
enforcement as well. We talked about it,
but it is not only limited to
monitoring, enforcement of application
at runtime, right. There is a complete
set of STLC security, and I was only
explaining the container side of
security here.
Right, now if we see
the entire STLC, right, it's a sort of
different toolings, different
environment, and we provide you all at
once over a single visibility where you
like security engineers, cloud
administrator, right,
Kubernetes admins, right, all can be
invited using different role-based
access control depending upon their
permissions and privilege, and then they
can manage the entire set of security
using one platform. So, that is just a
one thing and different aspects of
looking into the security.
Okay, okay. So,
let's make this real for the audience,
Aditya. So, let's quickly jump into the
environments and the industries where
this
problem shows up most acutely.
So, if you could have comment on that.
Yeah, surely I do have comment on that.
Uh
Just a second.
After that, uh Aditya, we will jump into
the right away
for the Q&A sessions because most of the
audience here, they are uh
very uh technical with this stuff and uh
they have multiple questions regarding
this. Uh we'll pick a few and uh
when you uh
then we can answer those questions.
Cool. Makes sense. Right. So, uh
basically, uh we were talking around the
different environments and the industry
that is having uh like some sort of
problems, right? Yeah, yeah. Yeah. So,
basically, it helps uh like mostly in
the three big areas, right? First would
be the finance, obviously, right? They
have very strict rules and uh need to
stay compliant all the times, right? Uh
then, second would be like in terms of
uh compliance, we get give them audit
trails, right? We help them get
compliant with industry uh regulatory
compliance framework. There is 35 plus
different compliances that we support,
right?
>> I think uh the GRC part is uh free of
charge with the AcuNox platform. Of
course, of course, it's completely free
of charge. Uh it comes with AcuNox and
GRC is something uh really important for
the finance sectors, right? And that is
where we help them get compliant
with respect to different compliances.
Right. Second would be the
manufacturing. They have uh very
critical take, right? On a factory
floor, they need visibility without
breaking the older systems, right? Older
system, I mean uh VM servers, bare
metals, right? So, in this case, eBPF is
very, very perfect for them. That
provides uh deep visibility over the app
behavior even in older systems. We
support that, right? It's uh like system
D based deployment in older systems like
VMs and uh bare metals. So, eBPF is
really perfect for to provide deep
visibility in those systems. Now, the
third one is fast-moving DevOps team.
Right? Where everything is automated.
They rely on us to catch security issues
early in their pipelines. It means the
one thing which I was explaining right
before this one, the entire STSS
security and pipeline security, right?
Whatever changes you are doing DevOps
team, right? Your developers, whatever
changes you are doing, it gets monitored
and be ensured that bad code never makes
into the production.
Mhm.
Right.
>> So, that were the three different
sectors where AccuKnox provides security
today.
Awesome. Awesome. So,
before jumping to the Q&A session, so
any message for the security teams
evaluating the hybrid
coverage today?
Any thoughts on that?
Yes, of course.
There is
Right. So, basically
the first thing is when we say security,
right? We always rely on different
tools, right? Everybody relies on tools,
right? Uh
when we talk tools, right? We should
never rely on a single tool for a single
use case. I'm saying this because uh
most of the time you see like uh if I
have to sell a tool, right? From my
perspective, if I have to sell one tool,
I'll just make sure that you see
everything is green at your end, right?
Like we are able to secure you. I'm able
to secure you for a different use case,
right? But uh
what I want to say here is basically you
have different tools yourself, right?
AccuKnox covers different security for
you, right? You get a holistic picture.
You can actually compare contrast
between different tools findings, right?
So, there is no green dashboard, it's
red for you, right? You need to work on
it and you need to make it green.
And that is how you remain secure.
Absolutely, absolutely. So, I think I
have let me check
a few questions actually. So, I think
the given time
we be able to like how many questions
that we able to answer Aditya, you tell
me.
Like one or two?
Uh
we can answer some from there. Let me
check as well. No,
like I can pick you one if you want. So,
um
Yes, please pick.
So, quick answer Aditya, what does
onboarding look like for a hybrid set of
three
200 nodes?
We'll go over onboarding.
Yeah, it's really a good one. 200 nodes
you have and you have a hybrid
environment, right? So, I think
onboarding is really super fast because
we don't usually use heavy agents,
right? Isn't it only there in case of
runtime security and that too is own
developed Q armor. It uses EVPF, you
know EVPF, we have talked about it. This
is a very light weight uh
deployment which will monitor your app
behavior. So, even if you have 200
nodes, deployment is really simple for
both Kubernetes and bare metal servers.
You can fully automate it for 200 nodes.
We can map out your whole environment in
just a few hours.
Right? And yeah, we use helm for the
deployment, so it's pretty
straightforward.
Got it, got it.
So, the given time constraint Aditya, so
we have to wind up the session for today
and thank you so much. That was uh one
of the clearest walkthroughs of the
hybrid security coverage I've seen here.
And uh thank you for everyone join us
today and
Um if you today's session rest specific
questions and about your environment uh
the Equinox is Equinox team is available
for personalized walkthrough.
Um I think Aditya and team can watch on
that and you can book a demo using the
link link in the description and for
those who uh you are in Sri Lanka, VS1
is your local partner. And feel free to
reach out us directly. And
uh I think we can wind up the session
for today and thank you again for
joining us. Stay secure and